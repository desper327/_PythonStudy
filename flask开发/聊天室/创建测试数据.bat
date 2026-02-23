@echo off
chcp 65001 >nul
echo ========================================
echo    Flask聊天室 - 创建测试数据
echo ========================================
echo.

cd /d "%~dp0backend"

echo 正在创建测试用户和群组...
echo.
python create_test_data.py

echo.
pause
