#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
数据库一键修复脚本
"""
import os
import sys
import subprocess

def run_command(cmd, description):
    """运行命令并处理结果"""
    print(f"\n{'='*60}")
    print(f"📋 {description}")
    print('='*60)
    
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            check=True,
            capture_output=False,
            text=True
        )
        print(f"✅ {description} - 成功！")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - 失败！")
        print(f"错误: {e}")
        return False

def main():
    print("="*60)
    print("🔧 WelfareWatch 数据库一键修复")
    print("="*60)
    print("\n此脚本将：")
    print("1. 删除并重建数据库")
    print("2. 生成迁移文件")
    print("3. 执行迁移")
    print("4. 初始化示例数据")
    print("\n⚠️  警告：此操作将删除所有现有数据！")
    
    response = input("\n确定继续吗？(输入 yes): ")
    if response.lower() != 'yes':
        print("操作已取消")
        sys.exit(0)
    
    # 步骤 1: 重建数据库
    print("\n" + "="*60)
    print("📋 步骤 1/4: 删除并重建数据库")
    print("="*60)
    print("请在 MySQL 提示符中输入密码...")
    
    sql_cmd = 'DROP DATABASE IF EXISTS welfarewatch; CREATE DATABASE welfarewatch CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;'
    result = subprocess.run(
        f'mysql -u root -p -e "{sql_cmd}"',
        shell=True
    )
    
    if result.returncode != 0:
        print("\n❌ 数据库操作失败！")
        print("   请检查：")
        print("   1. MySQL 是否运行：net start MySQL80")
        print("   2. 密码是否正确")
        sys.exit(1)
    
    print("✅ 数据库重建成功！")
    
    # 步骤 2: 生成迁移文件
    if not run_command("python manage.py makemigrations", "步骤 2/4: 生成迁移文件"):
        sys.exit(1)
    
    # 步骤 3: 执行迁移
    if not run_command("python manage.py migrate", "步骤 3/4: 执行数据库迁移"):
        sys.exit(1)
    
    # 步骤 4: 初始化数据
    print("\n" + "="*60)
    print("📋 步骤 4/4: 初始化示例数据")
    print("="*60)
    
    init_result = subprocess.run("python init_data.py", shell=True)
    if init_result.returncode == 0:
        print("✅ 示例数据初始化成功！")
    else:
        print("⚠️  初始化数据失败（可能已经有数据）")
    
    # 完成
    print("\n" + "="*60)
    print("🎉 修复完成！")
    print("="*60)
    print("\n📋 测试账号：")
    print("   管理员: admin / admin123")
    print("   审核员: moderator / moderator123")
    print("   用户  : user1 / password123")
    print("\n🚀 下一步：")
    print("   python manage.py runserver")
    print("\n然后访问：")
    print("   前端: http://localhost:5173")
    print("   后端: http://localhost:8000")
    print("   API文档: http://localhost:8000/api/docs/")
    print()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n操作已取消")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n❌ 发生错误: {e}")
        sys.exit(1)

