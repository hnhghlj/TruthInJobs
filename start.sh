#!/bin/bash

# WelfareWatch 启动脚本

echo "=================================="
echo "   WelfareWatch 启动脚本"
echo "=================================="

echo ""
echo "⚠️  重要：请确保已安装并启动 MySQL 数据库！"
echo "   数据库名: welfarewatch"
echo "   详细配置请查看: backend/MYSQL_SETUP.md"
echo ""
read -p "按 Enter 键继续..."

# 检查 Python 是否安装
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误: 未找到 Python3，请先安装 Python"
    exit 1
fi

# 检查 Node.js 是否安装
if ! command -v node &> /dev/null; then
    echo "❌ 错误: 未找到 Node.js，请先安装 Node.js"
    exit 1
fi

echo ""
echo "1. 初始化后端..."
echo "=================================="

cd backend

# 创建虚拟环境
if [ ! -d "venv" ]; then
    echo "创建虚拟环境..."
    python3 -m venv venv
fi

# 激活虚拟环境
source venv/bin/activate

# 安装依赖
echo "安装 Python 依赖..."
pip install -r requirements.txt

# 数据库迁移
echo "执行数据库迁移..."
python manage.py makemigrations
python manage.py migrate

# 询问是否初始化示例数据
read -p "是否初始化示例数据？(y/n): " init_data
if [ "$init_data" = "y" ] || [ "$init_data" = "Y" ]; then
    echo "初始化示例数据..."
    python init_data.py
fi

# 启动后端服务
echo ""
echo "启动后端服务..."
python manage.py runserver &
BACKEND_PID=$!

cd ..

echo ""
echo "2. 初始化前端..."
echo "=================================="

cd frontend

# 安装依赖
if [ ! -d "node_modules" ]; then
    echo "安装 npm 依赖..."
    npm install
fi

# 启动前端服务
echo "启动前端服务..."
npm run dev &
FRONTEND_PID=$!

cd ..

echo ""
echo "=================================="
echo "✅ 启动完成！"
echo "=================================="
echo ""
echo "📋 访问地址："
echo "   前端: http://localhost:5173"
echo "   后端API: http://localhost:8000/api/"
echo "   API文档: http://localhost:8000/api/docs/"
echo ""
echo "👤 登录信息："
echo "   管理员: admin / admin123"
echo "   审核员: moderator / moderator123"
echo "   用户: user1 / password123"
echo ""
echo "🛑 按 Ctrl+C 停止服务"
echo "=================================="
echo ""

# 等待用户中断
wait

