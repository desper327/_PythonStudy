# -*- coding: utf-8 -*-
from pathlib import Path
from typing import List, Sequence, Tuple
import shutil
import tempfile

import pyzipper


def _zip_single_input(
    input_path: Path,
    zip_path: Path,
    password: str
) -> None:
    """
    将单个输入（文件或目录）压缩为一个带密码zip。
    """
    pwd_bytes = password.encode("utf-8")

    with pyzipper.AESZipFile(
        str(zip_path),
        mode="w",
        compression=pyzipper.ZIP_DEFLATED,
        encryption=pyzipper.WZ_AES
    ) as zf:
        zf.setpassword(pwd_bytes)
        zf.setencryption(pyzipper.WZ_AES, nbits=256)

        if input_path.is_file():
            zf.write(str(input_path), arcname=input_path.name)
            return

        # 目录递归
        base_parent = input_path.parent
        for p in input_path.rglob("*"):
            if p.is_file():
                arcname = str(p.relative_to(base_parent)).replace("\\", "/")
                zf.write(str(p), arcname=arcname)


def nested_compress_with_passwords(
    source_path: str,
    passwords: Sequence[str],
    output_dir: str,
    base_name: str = "nested_archive",
    keep_all_layers: bool = True
) -> Tuple[Path, List[Path]]:
    """
    按密码列表进行嵌套多次压缩（次数=密码数量）。
    第 i 次压缩使用 passwords[i]。

    Args:
        source_path: 要压缩的文件或目录
        passwords: 密码列表
        output_dir: 输出目录
        base_name: 输出基础名
        keep_all_layers: 是否保留中间层zip

    Returns:
        (最终zip路径, 全部层zip列表)
    """
    if not passwords:
        raise ValueError("passwords 不能为空")

    src = Path(source_path).expanduser().resolve()
    if not src.exists():
        raise FileNotFoundError("source_path 不存在: {0}".format(src))

    out_dir = Path(output_dir).expanduser().resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    layer_paths: List[Path] = []

    current_input = src
    for index, password in enumerate(passwords, start=1):
        layer_zip = out_dir / "{0}_layer_{1:02d}.zip".format(base_name, index)
        _zip_single_input(current_input, layer_zip, str(password))
        layer_paths.append(layer_zip)
        current_input = layer_zip

    final_zip = layer_paths[-1]

    # 不保留中间层
    if not keep_all_layers:
        for p in layer_paths[:-1]:
            if p.exists():
                p.unlink()
        layer_paths = [final_zip]

    return final_zip, layer_paths


def nested_extract_with_passwords(
    final_zip_path: str,
    passwords: Sequence[str],
    output_dir: str
) -> Path:
    """
    按密码列表反向逐层解压嵌套zip。
    注意：解压顺序是 passwords 的倒序（最后一层先解）。

    Args:
        final_zip_path: 最外层zip（最终产物）
        passwords: 压缩时使用的密码列表（原顺序）
        output_dir: 最终解压目录

    Returns:
        最终内容目录路径
    """
    if not passwords:
        raise ValueError("passwords 不能为空")

    current_zip = Path(final_zip_path).expanduser().resolve()
    if not current_zip.exists():
        raise FileNotFoundError("final_zip_path 不存在: {0}".format(current_zip))

    out_dir = Path(output_dir).expanduser().resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory() as tmp_root:
        tmp_root_path = Path(tmp_root)

        # 逐层解压：最后一层密码先用
        for layer_index, password in enumerate(reversed(passwords), start=1):
            layer_out = tmp_root_path / "extract_layer_{0:02d}".format(layer_index)
            layer_out.mkdir(parents=True, exist_ok=True)

            with pyzipper.AESZipFile(str(current_zip), mode="r") as zf:
                zf.setpassword(str(password).encode("utf-8"))
                zf.extractall(str(layer_out))

            # 不是最后一次时，应当只得到一个内层zip
            if layer_index < len(passwords):
                inner_zips = [p for p in layer_out.iterdir() if p.is_file() and p.suffix.lower() == ".zip"]
                if len(inner_zips) != 1:
                    raise RuntimeError(
                        "第{0}层解压后未找到唯一内层zip，实际数量: {1}".format(layer_index, len(inner_zips))
                    )
                current_zip = inner_zips[0]
            else:
                # 最后一层：把内容拷贝到output_dir
                for item in layer_out.iterdir():
                    target = out_dir / item.name
                    if item.is_dir():
                        shutil.copytree(str(item), str(target), dirs_exist_ok=True)
                    else:
                        shutil.copy2(str(item), str(target))

    return out_dir


if __name__ == "__main__":
    # 示例
    source = r"D:\ttt\max_packages"  # 文件或目录都可以
    pwds = ["","",""]
    out_zip_dir = r"D:\demo_zip_out"
    out_extract_dir = r"D:\demo_zip_extract"

    final_zip, all_layers = nested_compress_with_passwords(
        source_path=source,
        passwords=pwds,
        output_dir=out_zip_dir,
        base_name="demo_nested",
        keep_all_layers=True
    )
    print("最终zip:", final_zip)
    print("所有层:", all_layers)
    #final_zip=r"D:\demo_zip_out\demo1_nested_layer_12.zip"

    extracted_dir = nested_extract_with_passwords(
        final_zip_path=str(final_zip),
        passwords=pwds,
        output_dir=out_extract_dir
    )
    print("最终解压目录:", extracted_dir)
    #_zip_single_input(Path(r"D:\ZY\netEase\4105"), Path(r"D:\demo_zip_out\test.zip"), "123")