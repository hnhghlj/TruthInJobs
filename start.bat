@echo off
chcp 65001 >nul
title WelfareWatch 启动脚本

echo ==================================
echo    WelfareWatch 启动脚本
echo ==================================

echo.
echo [重要] 请确保已安装并启动 MySQL 数据库！
echo        数据库名: welfarewatch
echo        详细配置请查看: backend\MYSQL_SETUP.md
echo.
pause

REM 检查 Python 是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 错误: 未找到 Python，请先安装 Python
    pause
    exit /b 1
)

REM 检查 Node.js 是否安装
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 错误: 未找到 Node.js，请先安装 Node.js
    pause
    exit /b 1
)

echo.
echo 1. 初始化后端...
echo ==================================

cd backend

REM 创建虚拟环境
if not exist "venv" (
    echo 创建虚拟环境...
    python -m venv venv
)

REM 激活虚拟环境
call venv\Scripts\activate.bat

REM 安装依赖
echo 安装 Python 依赖...
pip install -r requirements.txt

REM 数据库迁移
echo 执行数据库迁移...
python manage.py makemigrations
python manage.py migrate

REM 询问是否初始化示例数据
set /p init_data="是否初始化示例数据？(y/n): "
if /i "%init_data%"=="y" (
    echo 初始化示例数据...
    python init_data.py
)

REM 启动后端服务
echo.
echo 启动后端服务...
start "WelfareWatch Backend" python manage.py runserver

cd ..

echo.
echo 2. 初始化前端...
echo ==================================

cd frontend

REM 安装依赖
if not exist "node_modules" (
    echo 安装 npm 依赖...
    npm install
)

REM 启动前端服务
echo 启动前端服务...
start "WelfareWatch Frontend" npm run dev

cd ..

echo.
echo ==================================
echo ✅ 启动完成！
echo ==================================
echo.
echo 📋 访问地址：
echo    前端: http://localhost:5173
echo    后端API: http://localhost:8000/api/
echo    API文档: http://localhost:8000/api/docs/
echo.
echo 👤 登录信息：
echo    管理员: admin / admin123
echo    审核员: moderator / moderator123
echo    用户: user1 / password123
echo.
echo 🛑 关闭命令窗口停止服务
echo ==================================
echo.

pause

