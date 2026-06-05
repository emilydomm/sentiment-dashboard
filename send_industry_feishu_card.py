#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
发送行业资讯飞书卡片（固定只发给馨姐个人飞书）

用法：
  python3 send_industry_feishu_card.py --date 2026-05-31
  python3 send_industry_feishu_card.py --date 2026-05-31 --dry-run
"""

import argparse
import json
import subprocess
from datetime import datetime
from pathlib import Path

TARGET = "user:ou_dfa6d78ac7f1e08b474d766109b9fea7"
DASHBOARD_URL = "https://emilydomm.github.io/sentiment-dashboard/"
BASE_DIR = Path('/workspace/sentiment-dashboard')
DATA_DIR = BASE_DIR / 'docs' / 'data' / 'industry'
LOG_DIR = BASE_DIR / 'logs'


def load_items(report_date: str):
    path = DATA_DIR / f'{report_date}.json'
    if not path.exists():
        raise FileNotFoundError(f'行业资讯文件不存在: {path}')
    data = json.loads(path.read_text(encoding='utf-8'))
    if not isinstance(data, list) or not data:
        raise ValueError(f'行业资讯文件为空或格式错误: {path}')
    return path, data


def trim(text: str, limit: int) -> str:
    text = ' '.join((text or '').split())
    return text if len(text) <= limit else text[: limit - 1] + '…'


def build_presentation(report_date: str, items: list[dict]):
    blocks = [
        {
            "type": "context",
            "text": f"📅 {report_date}｜共 {len(items)} 条｜仅发送最终资讯与看板链接"
        },
        {"type": "divider"},
    ]

    for idx, item in enumerate(items[:8], 1):
        keyword = item.get('keyword') or '行业资讯'
        title = trim(item.get('title') or '未命名资讯', 72)
        desc = trim(item.get('desc') or '', 100)
        publish_date = item.get('publish_date') or '未知日期'
        url = item.get('url') or DASHBOARD_URL
        line = f"{idx}. 【{keyword}】{title}\n{publish_date}｜{desc}\n原文：{url}"
        blocks.append({"type": "text", "text": line})

    blocks.extend([
        {"type": "divider"},
        {
            "type": "buttons",
            "buttons": [
                {
                    "label": "查看看板",
                    "url": DASHBOARD_URL,
                    "style": "primary"
                }
            ]
        }
    ])

    return {
        "title": f"📰 今日行业资讯｜{report_date}",
        "tone": "info",
        "blocks": blocks,
    }


def append_log(report_date: str, message: str):
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    log_path = LOG_DIR / f'industry_{report_date}.log'
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with log_path.open('a', encoding='utf-8') as f:
        f.write(f'[{timestamp}] {message}\n')


def send_card(report_date: str, presentation: dict, dry_run: bool):
    payload = {
        "action": "send",
        "channel": "feishu",
        "target": TARGET,
        "presentation": presentation,
    }

    if payload["target"] != TARGET or not payload["target"].startswith("user:"):
        append_log(report_date, f'发送失败：目标非法，必须且只能是 {TARGET}')
        raise ValueError(f"发送目标非法，必须且只能是馨姐个人飞书: {TARGET}")

    append_log(report_date, f'开始发送飞书卡片，目标={TARGET}，dry_run={str(dry_run).lower()}')
    print(json.dumps(payload, ensure_ascii=False, indent=2))

    cmd = [
        "openclaw", "message", "send",
        "--channel", "feishu",
        "--target", TARGET,
        "--presentation", json.dumps(presentation, ensure_ascii=False),
    ]

    if dry_run:
        cmd.append("--dry-run")

    result = subprocess.run(cmd, capture_output=True, text=True, check=False)
    stdout = (result.stdout or '').strip()
    stderr = (result.stderr or '').strip()

    if stdout:
        print(stdout)
        append_log(report_date, f'发送返回: {stdout}')
    if result.returncode != 0:
        if stderr:
            print(stderr)
            append_log(report_date, f'发送报错: {stderr}')
        append_log(report_date, f'发送失败，exit_code={result.returncode}')
        raise SystemExit(result.returncode)

    append_log(report_date, '发送完成')
    return 0


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--date', required=True, help='行业资讯日期 YYYY-MM-DD')
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()

    _, items = load_items(args.date)
    presentation = build_presentation(args.date, items)
    return send_card(args.date, presentation, args.dry_run)


if __name__ == '__main__':
    raise SystemExit(main())
