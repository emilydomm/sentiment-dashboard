#!/bin/bash
# 每日行业资讯自动抓取脚本
# 每天08:30运行，通过OpenClaw Agent调用web_search生成行业资讯

set -e

DATE=$(date +%Y-%m-%d)
LOG_FILE="/workspace/sentiment-dashboard/logs/industry_${DATE}.log"
mkdir -p /workspace/sentiment-dashboard/logs

echo "[$(date '+%Y-%m-%d %H:%M:%S')] 开始抓取行业资讯..." >> "$LOG_FILE"

# 调用OpenClaw会话发送消息给Agent执行抓取任务
# 注意：这需要OpenClaw API或消息队列支持

# 临时方案：通过Python脚本调用web_search
python3 << 'PYTHON_SCRIPT'
import sys
sys.path.insert(0, '/workspace/sentiment-dashboard')

# 这里需要实际调用OpenClaw的web_search工具
# 由于脚本环境无法直接调用工具，需要通过其他方式触发

# 方案：创建一个标记文件，让heartbeat检查并执行
import json
from datetime import date

flag_file = '/workspace/sentiment-dashboard/.industry_task_pending'
task_data = {
    'date': date.today().strftime('%Y-%m-%d'),
    'status': 'pending',
    'keywords': ['底盘', '电池', '电机', '增程', '充电', '三电', '能耗', '悬架']
}

with open(flag_file, 'w') as f:
    json.dump(task_data, f, ensure_ascii=False, indent=2)

print(f"[INFO] 已创建任务标记: {flag_file}")
PYTHON_SCRIPT

echo "[$(date '+%Y-%m-%d %H:%M:%S')] 任务标记已创建，等待Agent执行" >> "$LOG_FILE"
