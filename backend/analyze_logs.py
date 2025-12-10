#!/usr/bin/env python
"""日志分析工具"""
from pathlib import Path
from collections import Counter, defaultdict
import re
from datetime import datetime
import sys


def analyze_logs(log_file='general.log', detailed=False):
    """分析日志文件"""
    log_path = Path('logs') / log_file
    
    if not log_path.exists():
        print(f"❌ 日志文件不存在: {log_path}")
        return
    
    try:
        with open(log_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except Exception as e:
        print(f"❌ 读取日志文件失败: {e}")
        return
    
    if not lines:
        print(f"📄 日志文件为空: {log_path}")
        return
    
    # 统计数据
    levels = Counter()
    modules = Counter()
    errors_by_module = defaultdict(int)
    hourly_stats = Counter()
    daily_stats = Counter()
    
    error_messages = []
    
    for line in lines:
        # 提取时间
        time_match = re.search(r'\[(\w+)\] ([\d-]+ [\d:]+)', line)
        if time_match:
            level = time_match.group(1)
            timestamp = time_match.group(2)
            
            levels[level] += 1
            
            # 按小时统计
            try:
                dt = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
                hour_key = dt.strftime('%Y-%m-%d %H:00')
                hourly_stats[hour_key] += 1
                daily_stats[dt.strftime('%Y-%m-%d')] += 1
            except:
                pass
        
        # 提取模块名
        module_match = re.search(r'\] (\S+) ', line)
        if module_match:
            module = module_match.group(1)
            modules[module] += 1
            
            # 统计各模块的错误
            if 'ERROR' in line or 'CRITICAL' in line:
                errors_by_module[module] += 1
        
        # 收集错误消息
        if 'ERROR' in line or 'CRITICAL' in line:
            error_messages.append(line.strip())
    
    # 打印分析报告
    print("=" * 80)
    print(f"📊 日志分析报告: {log_file}")
    print("=" * 80)
    print(f"\n📈 基本统计:")
    print(f"   总日志条数: {len(lines):,}")
    
    file_size = log_path.stat().st_size / 1024 / 1024
    print(f"   文件大小: {file_size:.2f} MB")
    
    if lines:
        first_line_time = re.search(r'[\d-]+ [\d:]+', lines[0])
        last_line_time = re.search(r'[\d-]+ [\d:]+', lines[-1])
        if first_line_time and last_line_time:
            print(f"   时间范围: {first_line_time.group()} 至 {last_line_time.group()}")
    
    # 日志级别统计
    print(f"\n📊 日志级别分布:")
    total = sum(levels.values())
    for level in ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']:
        count = levels.get(level, 0)
        if count > 0:
            percentage = count / total * 100 if total > 0 else 0
            bar_length = int(percentage / 2)
            bar = '█' * bar_length
            print(f"   {level:10s}: {count:6,d} ({percentage:5.1f}%) {bar}")
    
    # 模块统计
    print(f"\n🔧 模块日志统计 (Top 10):")
    for module, count in modules.most_common(10):
        percentage = count / len(lines) * 100 if len(lines) > 0 else 0
        print(f"   {module:40s}: {count:6,d} ({percentage:5.1f}%)")
    
    # 错误统计
    if errors_by_module:
        print(f"\n⚠️  模块错误统计:")
        for module, count in sorted(errors_by_module.items(), key=lambda x: x[1], reverse=True)[:10]:
            print(f"   {module:40s}: {count:6,d} 个错误")
    
    # 每日统计
    if daily_stats:
        print(f"\n📅 每日日志统计:")
        for day in sorted(daily_stats.keys())[-7:]:  # 最近7天
            count = daily_stats[day]
            bar_length = min(int(count / max(daily_stats.values()) * 50), 50)
            bar = '█' * bar_length
            print(f"   {day}: {count:6,d} {bar}")
    
    # 详细错误信息
    if detailed and error_messages:
        print(f"\n🚨 最近的错误 (最多显示10条):")
        for error_msg in error_messages[-10:]:
            print(f"   {error_msg}")
    
    print("\n" + "=" * 80)
    
    # 生成建议
    print(f"\n💡 分析建议:")
    
    error_rate = levels.get('ERROR', 0) + levels.get('CRITICAL', 0)
    if error_rate > len(lines) * 0.1:
        print(f"   ⚠️  错误率较高 ({error_rate / len(lines) * 100:.1f}%)，建议检查系统")
    
    if levels.get('CRITICAL', 0) > 0:
        print(f"   🚨 发现 {levels['CRITICAL']} 个 CRITICAL 级别错误，需要立即处理！")
    
    if file_size > 50:
        print(f"   💾 日志文件较大 ({file_size:.1f} MB)，建议清理旧日志")
    
    print("=" * 80)


def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description='WelfareWatch 日志分析工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
示例:
  python analyze_logs.py                    # 分析 general.log
  python analyze_logs.py error.log          # 分析 error.log
  python analyze_logs.py general.log -d     # 显示详细错误信息
        '''
    )
    
    parser.add_argument(
        'log_file',
        nargs='?',
        default='general.log',
        choices=['general.log', 'error.log', 'database.log', 'security.log'],
        help='日志文件名称 (默认: general.log)'
    )
    parser.add_argument(
        '-d', '--detailed',
        action='store_true',
        help='显示详细错误信息'
    )
    
    args = parser.parse_args()
    analyze_logs(args.log_file, args.detailed)


if __name__ == '__main__':
    main()

