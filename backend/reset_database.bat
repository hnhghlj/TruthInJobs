@echo off
chcp 65001 >nul
echo ============================================================
echo 重置数据库脚本
echo ============================================================
echo.
echo ⚠️  警告：此操作将删除所有数据！
echo.
set /p confirm="确定要继续吗？(输入 yes 继续): "

if not "%confirm%"=="yes" (
    echo 操作已取消
    exit /b
)

echo.
echo 📋 步骤 1/5: 删除旧的迁移文件...
for /d %%d in (apps\*) do (
    if exist "%%d\migrations" (
        echo 清理 %%d\migrations...
        del /q "%%d\migrations\*.py" 2>nul
        echo. > "%%d\migrations\__init__.py"
    )
)

echo.
echo 📋 步骤 2/5: 删除数据库...
echo 请输入 MySQL root 密码
mysql -u root -p -e "DROP DATABASE IF EXISTS welfarewatch; CREATE DATABASE welfarewatch CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"

if errorlevel 1 (
    echo ❌ 数据库删除失败，请检查 MySQL 是否运行
    pause
    exit /b 1
)

echo.
echo 📋 步骤 3/5: 生成迁移文件...
python manage.py makemigrations

if errorlevel 1 (
    echo ❌ 生成迁移文件失败
    pause
    exit /b 1
)

echo.
echo 📋 步骤 4/5: 执行迁移...
python manage.py migrate

if errorlevel 1 (
    echo ❌ 执行迁移失败
    pause
    exit /b 1
)

echo.
echo 📋 步骤 5/5: 初始化示例数据...
set /p init_data="是否初始化示例数据？(输入 yes 继续): "

if "%init_data%"=="yes" (
    python init_data.py
)

echo.
echo ============================================================
echo ✅ 数据库重置完成！
echo ============================================================
echo.
echo 下一步：
echo   python manage.py runserver
echo.
pause

