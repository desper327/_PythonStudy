@echo off
chcp 65001 >nul
echo ========================================
echo    Flask聊天室 - 启动前端客户端
echo ========================================
echo.

cd /d "%~dp0frontend"

echo 检查Python环境...
python --version
if %errorlevel% neq 0 (
    echo [错误] 未找到Python，请先安装Python 3.8+
    pause
    exit /b 1
)

echo.
echo 检查依赖包...
python -c "import PySide6" 2>nul
if %errorlevel% neq 0 (
    echo [警告] 未安装依赖包，正在安装...
    pip install -r requirements.txt
)

echo.
echo 启动前端客户端...
echo 请确保后端服务器已启动！
echo.
python main.py

pause
