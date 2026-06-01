#!/bin/bash
# 每日行业资讯自动抓取脚本
# 每天08:30运行，通过OpenClaw Agent调用web_search生成行业资讯

set -e

DATE=$(date +%Y-%m-%d)
LOG_FILE="/workspace/sentiment-dashboard/logs/industry_${DATE}.log"
mkdir -p /workspace/sentiment-dashboard/logs

echo "[$(date '+%Y-%m-%d %H:%M:%S')] 开始抓取行业资讯..." >> "$LOG_FILE"

python3 << 'PYTHON_SCRIPT'
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

INDUSTRY_JSON="/workspace/sentiment-dashboard/docs/data/industry/${DATE}.json"
CARD_SCRIPT="/workspace/sentiment-dashboard/send_industry_feishu_card.py"

if [ -f "$INDUSTRY_JSON" ]; then
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] 检测到行业资讯文件已存在，生成飞书卡片 payload" >> "$LOG_FILE"
  if [ ! -f "$CARD_SCRIPT" ]; then
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] 缺少卡片脚本，终止执行" >> "$LOG_FILE"
    exit 1
  fi
  python3 "$CARD_SCRIPT" --date "$DATE" >> "$LOG_FILE" 2>&1 || exit 1
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] 卡片 payload 已生成；禁止回退普通文本发送" >> "$LOG_FILE"
fi
