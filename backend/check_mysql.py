#!/usr/bin/env python
"""检查 MySQL 连接和配置"""
import sys
import os
import logging

# 设置 Django 环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'welfare_watch.settings')

try:
    import django
    django.setup()
except Exception as e:
    print(f"❌ Django 设置失败: {e}")
    sys.exit(1)

from django.db import connection
from django.core.management import execute_from_command_line

# 配置日志
logger = logging.getLogger('scripts')


def check_mysql_connection():
    """检查 MySQL 连接"""
    logger.info("=" * 60)
    logger.info("MySQL 连接检查")
    logger.info("=" * 60)
    
    # 控制台输出
    print("=" * 60)
    print("MySQL 连接检查")
    print("=" * 60)
    
    try:
        # 尝试连接数据库
        with connection.cursor() as cursor:
            cursor.execute("SELECT VERSION()")
            version = cursor.fetchone()[0]
            logger.info(f"MySQL 连接成功，版本: {version}")
            print(f"\n✅ MySQL 连接成功！")
            print(f"   版本: {version}")
            
            # 检查数据库字符集
            cursor.execute("""
                SELECT 
                    DEFAULT_CHARACTER_SET_NAME,
                    DEFAULT_COLLATION_NAME 
                FROM information_schema.SCHEMATA 
                WHERE SCHEMA_NAME = DATABASE()
            """)
            charset, collation = cursor.fetchone()
            logger.info(f"数据库字符集: {charset}, 排序规则: {collation}")
            print(f"\n✅ 数据库字符集配置正确")
            print(f"   字符集: {charset}")
            print(f"   排序规则: {collation}")
            
            # 检查数据库名称
            cursor.execute("SELECT DATABASE()")
            db_name = cursor.fetchone()[0]
            logger.info(f"当前数据库: {db_name}")
            print(f"\n✅ 当前数据库: {db_name}")
            
            # 检查表是否存在
            cursor.execute("""
                SELECT COUNT(*) 
                FROM information_schema.tables 
                WHERE table_schema = DATABASE()
            """)
            table_count = cursor.fetchone()[0]
            
            if table_count == 0:
                logger.warning("数据库中没有表，需要运行迁移")
                print("\n⚠️  数据库中没有表")
                print("   请运行: python manage.py migrate")
            else:
                logger.info(f"数据库中有 {table_count} 个表")
                print(f"\n✅ 数据库中有 {table_count} 个表")
                
                # 列出主要的表
                cursor.execute("""
                    SELECT table_name 
                    FROM information_schema.tables 
                    WHERE table_schema = DATABASE()
                    AND table_name IN ('users', 'companies', 'reviews', 'comments')
                """)
                tables = cursor.fetchall()
                if tables:
                    print("   主要表:")
                    for table in tables:
                        print(f"   - {table[0]}")
                        logger.debug(f"发现表: {table[0]}")
            
            logger.info("MySQL 连接检查完成，所有配置正确")
            print("\n" + "=" * 60)
            print("✅ 所有检查通过！数据库配置正确。")
            print("=" * 60)
            return True
            
    except Exception as e:
        logger.error(f"MySQL 连接失败: {e}", exc_info=True)
        
        print("\n" + "=" * 60)
        print("❌ MySQL 连接失败！")
        print("=" * 60)
        print(f"\n错误信息: {e}")
        print("\n可能的原因：")
        print("1. MySQL 服务未启动")
        print("   解决方法: ")
        print("   - Windows: net start MySQL80")
        print("   - Linux: sudo systemctl start mysql")
        print("   - macOS: brew services start mysql")
        print("\n2. 数据库不存在")
        print("   解决方法: mysql -u root -p < backend/setup_mysql.sql")
        print("\n3. 用户名或密码错误")
        print("   解决方法: 检查 settings.py 中的数据库配置")
        print("\n4. 连接被拒绝")
        print("   解决方法: 检查 MySQL 是否监听 localhost:3306")
        print("\n详细配置指南请查看: backend/MYSQL_SETUP.md")
        print("详细日志请查看: logs/general.log")
        print("=" * 60)
        return False


def show_config():
    """显示当前配置"""
    from django.conf import settings
    
    logger.info("显示数据库配置")
    print("\n当前数据库配置：")
    print("-" * 60)
    db_config = settings.DATABASES['default']
    print(f"引擎:   {db_config.get('ENGINE')}")
    print(f"数据库: {db_config.get('NAME')}")
    print(f"用户:   {db_config.get('USER')}")
    print(f"主机:   {db_config.get('HOST')}")
    print(f"端口:   {db_config.get('PORT')}")
    print("-" * 60)
    
    logger.debug(f"数据库配置: {db_config}")


if __name__ == '__main__':
    try:
        show_config()
        
        if check_mysql_connection():
            print("\n🎉 恭喜！你可以开始使用 WelfareWatch 了！")
            print("\n下一步：")
            print("1. python manage.py migrate    # 创建数据表")
            print("2. python init_data.py          # 初始化示例数据")
            print("3. python manage.py runserver   # 启动开发服务器\n")
            logger.info("MySQL 检查成功完成")
        else:
            logger.error("MySQL 检查失败")
            sys.exit(1)
    except KeyboardInterrupt:
        logger.info("用户中断检查")
        print("\n\n检查已取消")
        sys.exit(0)
    except Exception as e:
        logger.error(f"检查过程发生未预期的错误: {e}", exc_info=True)
        print(f"\n发生错误: {e}")
        print("详细日志请查看: logs/error.log")
        sys.exit(1)
