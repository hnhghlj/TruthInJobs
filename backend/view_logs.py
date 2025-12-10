#!/usr/bin/env python
"""日志查看工具"""
import argparse
from pathlib import Path
import sys


def view_logs(log_file, lines=50, search=None, level=None, follow=False):
    """查看日志文件"""
    log_path = Path('logs') / log_file
    
    if not log_path.exists():
        print(f"❌ 日志文件不存在: {log_path}")
        print(f"   提示: 请先运行程序生成日志文件")
        return
    
    try:
        with open(log_path, 'r', encoding='utf-8') as f:
            all_lines = f.readlines()
    except Exception as e:
        print(f"❌ 读取日志文件失败: {e}")
        return
    
    if not all_lines:
        print(f"📄 日志文件为空: {log_path}")
        return
    
    # 过滤
    filtered_lines = all_lines
    if search:
        filtered_lines = [line for line in filtered_lines if search.lower() in line.lower()]
    if level:
        filtered_lines = [line for line in filtered_lines if f"[{level}]" in line]
    
    if not filtered_lines:
        print(f"📭 没有找到匹配的日志")
        return
    
    # 显示统计信息
    print("=" * 80)
    print(f"📋 日志文件: {log_file}")
    print(f"📊 总行数: {len(all_lines)}")
    if search or level:
        print(f"🔍 匹配行数: {len(filtered_lines)}")
    print(f"👁️  显示最后 {min(lines, len(filtered_lines))} 行")
    print("=" * 80)
    print()
    
    # 显示最后 N 行
    for line in filtered_lines[-lines:]:
        # 添加颜色（如果终端支持）
        if '[ERROR]' in line or '[CRITICAL]' in line:
            print(f"\033[91m{line.rstrip()}\033[0m")  # 红色
        elif '[WARNING]' in line:
            print(f"\033[93m{line.rstrip()}\033[0m")  # 黄色
        elif '[INFO]' in line:
            print(f"\033[92m{line.rstrip()}\033[0m")  # 绿色
        else:
            print(line.rstrip())
    
    print()
    print("=" * 80)


def list_logs():
    """列出所有日志文件"""
    logs_dir = Path('logs')
    
    if not logs_dir.exists():
        print("❌ logs 目录不存在")
        return
    
    log_files = list(logs_dir.glob('*.log*'))
    
    if not log_files:
        print("📭 没有找到日志文件")
        return
    
    print("=" * 80)
    print("📚 可用的日志文件:")
    print("=" * 80)
    
    for log_file in sorted(log_files):
        size = log_file.stat().st_size
        size_mb = size / 1024 / 1024
        modified = log_file.stat().st_mtime
        
        from datetime import datetime
        modified_time = datetime.fromtimestamp(modified).strftime('%Y-%m-%d %H:%M:%S')
        
        print(f"📄 {log_file.name:30s}  {size_mb:>8.2f} MB  {modified_time}")
    
    print("=" * 80)


def main():
    parser = argparse.ArgumentParser(
        description='WelfareWatch 日志查看工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
示例:
  python view_logs.py general.log                    # 查看一般日志
  python view_logs.py error.log -n 100               # 查看最后100行错误日志
  python view_logs.py general.log -s "user_id"       # 搜索包含user_id的日志
  python view_logs.py general.log -l ERROR           # 只显示ERROR级别日志
  python view_logs.py --list                         # 列出所有日志文件
        '''
    )
    
    parser.add_argument(
        'log_file',
        nargs='?',
        choices=['general.log', 'error.log', 'database.log', 'security.log'],
        help='日志文件名称'
    )
    parser.add_argument(
        '-n', '--lines',
        type=int,
        default=50,
        help='显示行数 (默认: 50)'
    )
    parser.add_argument(
        '-s', '--search',
        help='搜索关键词'
    )
    parser.add_argument(
        '-l', '--level',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
        help='过滤日志级别'
    )
    parser.add_argument(
        '--list',
        action='store_true',
        help='列出所有日志文件'
    )
    
    args = parser.parse_args()
    
    if args.list:
        list_logs()
    elif args.log_file:
        view_logs(args.log_file, args.lines, args.search, args.level)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()

