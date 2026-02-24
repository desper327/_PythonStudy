"""
子进程执行器 - 使用 QProcess 执行外部命令/脚本
目标：
1) 类似 MVC_通用基础/services/worker_thread.py 的风格（统一 SignalData 分发）
2) 让 Controller 能方便实现常用子进程功能：启动/停止、读 stdout/stderr、写 stdin、拿退出码等
3) SignalData.params 使用 dict（命名参数），便于 controller 用 handler(**params)
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Union

from Qt.QtCore import QObject, QProcess, Signal

from models.data_models import SignalData, ProcessSpec


class ProcessWorker(QObject):
    """
    基于 QProcess 的子进程执行器（QObject，不是线程）
    - 适合：调用 python 脚本、git、ffmpeg、curl、自定义 exe 等
    - 信号统一走 process_signal: Signal(SignalData)
    """

    process_signal = Signal(SignalData)

    def __init__(self, parent: Optional[QObject] = None):
        super().__init__(parent)

        self._proc = QProcess(self)
        self._spec: Optional[ProcessSpec] = None
        self._encoding: str = "utf-8"

        self._proc.started.connect(self._on_started)
        self._proc.finished.connect(self._on_finished)
        self._proc.readyReadStandardOutput.connect(self._on_ready_read_stdout)
        self._proc.readyReadStandardError.connect(self._on_ready_read_stderr)
        self._proc.errorOccurred.connect(self._on_error_occurred)
        self._proc.stateChanged.connect(self._on_state_changed)

    # -------------------------
    # Public API
    # -------------------------
    def is_running(self) -> bool:
        return self._proc.state() != QProcess.NotRunning

    def pid(self) -> int:
        try:
            return int(self._proc.processId())
        except Exception:
            return 0

    def start(self, spec: ProcessSpec) -> bool:
        """
        启动进程。成功返回 True（不代表进程一定会正常退出，只代表开始启动流程）。
        """
        if self.is_running():
            return False

        self._spec = spec
        self._encoding = spec.text_encoding or "utf-8"

        if spec.merge_channels:
            self._proc.setProcessChannelMode(QProcess.MergedChannels)
        else:
            self._proc.setProcessChannelMode(QProcess.SeparateChannels)

        if spec.working_directory:
            self._proc.setWorkingDirectory(spec.working_directory)

        if spec.environment:
            env = self._proc.processEnvironment()
            for k, v in spec.environment.items():
                env.insert(k, v)
            self._proc.setProcessEnvironment(env)

        if spec.start_detached:
            ok = QProcess.startDetached(spec.program, spec.arguments, spec.working_directory or "")
            self.process_signal.emit(
                SignalData(
                    signal_type="on_process_detached_started",
                    params={
                        "ok": bool(ok),
                        "program": spec.program,
                        "arguments": list(spec.arguments),
                        "working_directory": spec.working_directory,
                    },
                )
            )
            return bool(ok)

        self.process_signal.emit(
            SignalData(
                signal_type="on_process_starting",
                params={
                    "program": spec.program,
                    "arguments": list(spec.arguments),
                    "working_directory": spec.working_directory,
                },
            )
        )

        self._proc.start(spec.program, spec.arguments)
        return True

    def write_text(self, text: str) -> bool:
        """
        向子进程 stdin 写入文本（需要子进程读取 stdin）。
        """
        if not self.is_running():
            return False
        data = text.encode(self._encoding, errors="replace")
        self._proc.write(data)
        return True

    def write_bytes(self, data: Union[bytes, bytearray]) -> bool:
        if not self.is_running():
            return False
        self._proc.write(bytes(data))
        return True

    def close_write_channel(self) -> None:
        """
        关闭 stdin（告诉子进程不会再写入）。
        """
        try:
            self._proc.closeWriteChannel()
        except Exception:
            pass

    def terminate(self) -> bool:
        """
        尝试温和退出（让子进程自行清理）。返回值代表是否触发了 terminate 调用。
        """
        if not self.is_running():
            return False
        self.process_signal.emit(SignalData(signal_type="on_process_terminating", params={"pid": self.pid()}))
        self._proc.terminate()
        return True

    def kill(self) -> bool:
        """
        强制杀进程（不保证子进程有机会清理）。
        """
        if not self.is_running():
            return False
        self.process_signal.emit(SignalData(signal_type="on_process_killing", params={"pid": self.pid()}))
        self._proc.kill()
        return True

    def stop(self, *, kill_after_ms: int = 1500) -> None:
        """
        常用的 stop 策略：
        - 先 terminate
        - 超时未退出则 kill
        """
        if not self.is_running():
            return

        self.terminate()
        finished = self._proc.waitForFinished(kill_after_ms)
        if not finished and self.is_running():
            self.kill()

    # -------------------------
    # Internal slots
    # -------------------------
    def _on_started(self) -> None:
        self.process_signal.emit(
            SignalData(
                signal_type="on_process_started",
                params={
                    "pid": self.pid(),
                    "program": self._spec.program if self._spec else "",
                    "arguments": list(self._spec.arguments) if self._spec else [],
                    "working_directory": self._spec.working_directory if self._spec else None,
                },
            )
        )

    def _on_finished(self, exit_code: int, exit_status: QProcess.ExitStatus) -> None:
        self.process_signal.emit(
            SignalData(
                signal_type="on_process_finished",
                params={
                    "exit_code": int(exit_code),
                    "exit_status": int(exit_status),
                    "pid": self.pid(),
                },
            )
        )

    def _on_ready_read_stdout(self) -> None:
        raw = bytes(self._proc.readAllStandardOutput())
        text = raw.decode(self._encoding, errors="replace")
        self.process_signal.emit(
            SignalData(
                signal_type="on_process_stdout",
                params={
                    "text": text,
                    "raw": raw,
                    "pid": self.pid(),
                },
            )
        )

    def _on_ready_read_stderr(self) -> None:
        raw = bytes(self._proc.readAllStandardError())
        text = raw.decode(self._encoding, errors="replace")
        self.process_signal.emit(
            SignalData(
                signal_type="on_process_stderr",
                params={
                    "text": text,
                    "raw": raw,
                    "pid": self.pid(),
                },
            )
        )

    def _on_error_occurred(self, err: QProcess.ProcessError) -> None:
        self.process_signal.emit(
            SignalData(
                signal_type="on_process_error",
                params={
                    "error": int(err),
                    "error_string": self._proc.errorString(),
                    "pid": self.pid(),
                },
            )
        )

    def _on_state_changed(self, state: QProcess.ProcessState) -> None:
        self.process_signal.emit(
            SignalData(
                signal_type="on_process_state_changed",
                params={
                    "state": int(state),
                    "pid": self.pid(),
                },
            )
        )