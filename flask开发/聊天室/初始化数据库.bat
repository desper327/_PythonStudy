@echo off
chcp 65001 >nul
echo ========================================
echo    Flask聊天室 - 初始化数据库
echo ========================================
echo.

cd /d "%~dp0backend"

echo 检查Python环境...
python --version
if %errorlevel% neq 0 (
    echo [错误] 未找到Python，请先安装Python 3.8+
    pause
    exit /b 1
)

echo.
echo 初始化数据库表...
python app.py init-db

if %errorlevel% equ 0 (
    echo.
    echo [成功] 数据库初始化完成！
) else (
    echo.
    echo [错误] 数据库初始化失败，请检查配置文件
)

echo.
pause
