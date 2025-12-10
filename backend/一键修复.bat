@echo off
chcp 65001 >nul
echo ============================================================
echo 🔧 WelfareWatch 数据库一键修复
echo ============================================================
echo.
echo 此脚本将：
echo 1. 删除并重建数据库
echo 2. 生成迁移文件
echo 3. 执行迁移
echo 4. 初始化示例数据
echo.
echo ⚠️  警告：此操作将删除所有现有数据！
echo.
pause

echo.
echo 📋 步骤 1/4: 删除并重建数据库...
echo 请输入 MySQL root 密码：
mysql -u root -p -e "DROP DATABASE IF EXISTS welfarewatch; CREATE DATABASE welfarewatch CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"

if errorlevel 1 (
    echo.
    echo ❌ 数据库操作失败！
    echo    请检查：
    echo    1. MySQL 是否运行：net start MySQL80
    echo    2. 密码是否正确
    echo.
    pause
    exit /b 1
)

echo ✅ 数据库重建成功！
echo.

echo 📋 步骤 2/4: 生成迁移文件...
python manage.py makemigrations

if errorlevel 1 (
    echo.
    echo ❌ 生成迁移文件失败！
    echo.
    pause
    exit /b 1
)

echo ✅ 迁移文件生成成功！
echo.

echo 📋 步骤 3/4: 执行数据库迁移...
python manage.py migrate

if errorlevel 1 (
    echo.
    echo ❌ 执行迁移失败！
    echo.
    pause
    exit /b 1
)

echo ✅ 数据库迁移成功！
echo.

echo 📋 步骤 4/4: 初始化示例数据...
python init_data.py

if errorlevel 1 (
    echo.
    echo ⚠️  初始化数据失败（可能已经有数据）
    echo.
) else (
    echo ✅ 示例数据初始化成功！
)

echo.
echo ============================================================
echo 🎉 修复完成！
echo ============================================================
echo.
echo 📋 测试账号：
echo    管理员: admin / admin123
echo    审核员: moderator / moderator123
echo    用户  : user1 / password123
echo.
echo 🚀 下一步：
echo    python manage.py runserver
echo.
echo 然后访问：
echo    前端: http://localhost:5173
echo    后端: http://localhost:8000
echo    API文档: http://localhost:8000/api/docs/
echo.
pause

