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
from pathlib import Path

TARGET = "user:ou_dfa6d78ac7f1e08b474d766109b9fea7"
DASHBOARD_URL = "https://emilydomm.github.io/sentiment-dashboard/"
BASE_DIR = Path('/workspace/sentiment-dashboard')
DATA_DIR = BASE_DIR / 'docs' / 'data' / 'industry'


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


def send_card(presentation: dict, dry_run: bool):
    payload = {
        "action": "send",
        "channel": "feishu",
        "target": TARGET,
        "presentation": presentation,
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--date', required=True, help='行业资讯日期 YYYY-MM-DD')
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()

    _, items = load_items(args.date)
    presentation = build_presentation(args.date, items)
    return send_card(presentation, args.dry_run)


if __name__ == '__main__':
    raise SystemExit(main())
