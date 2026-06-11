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
STRICT_TEXT = (
    "行业资讯发送硬约束：仅允许发送飞书卡片；"
    f"目标必须且只能是 {TARGET}；"
    "禁止普通文本、禁止群聊、禁止过程说明。"
)


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


def normalize_items(report_date: str, items):
    if not isinstance(items, list) or not items:
        append_log(report_date, '发送失败：行业资讯数据不是非空列表')
        raise ValueError('行业资讯数据不是非空列表，禁止发送')
    normalized = []
    for idx, item in enumerate(items, 1):
        if isinstance(item, dict):
            normalized.append(item)
            continue
        append_log(report_date, f'发送失败：第 {idx} 条不是对象，类型={type(item).__name__}')
        raise ValueError(f'行业资讯第 {idx} 条不是对象，禁止发送')
    return normalized


def build_feishu_card(report_date: str, items: list[dict]):
    items = normalize_items(report_date, items)
    elements = [
        {
            "tag": "markdown",
            "content": f"📅 {report_date}｜共 {len(items)} 条｜仅发送最终资讯与看板链接"
        },
        {"tag": "hr"},
    ]

    for idx, item in enumerate(items[:8], 1):
        keyword = trim(item.get('keyword') or '行业资讯', 20)
        title = trim(item.get('title') or '未命名资讯', 72)
        desc = trim(item.get('desc') or '', 100)
        publish_date = item.get('publish_date') or '未知日期'
        url = item.get('url') or DASHBOARD_URL
        text = (
            f"**{idx}. 【{keyword}】{title}**\n"
            f"{publish_date}｜{desc}\n"
            f"[原文链接]({url})"
        )
        elements.append({"tag": "markdown", "content": text})

    elements.extend([
        {"tag": "hr"},
        {
            "tag": "action",
            "actions": [
                {
                    "tag": "button",
                    "text": {"tag": "plain_text", "content": "查看看板"},
                    "type": "primary",
                    "multi_url": {"url": DASHBOARD_URL}
                }
            ]
        }
    ])

    return {
        "schema": "2.0",
        "config": {"width_mode": "fill"},
        "header": {
            "title": {"tag": "plain_text", "content": f"📰 今日行业资讯｜{report_date}"},
            "template": "blue"
        },
        "body": {"elements": elements}
    }


def append_log(report_date: str, message: str):
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    log_path = LOG_DIR / f'industry_{report_date}.log'
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with log_path.open('a', encoding='utf-8') as f:
        f.write(f'[{timestamp}] {message}\n')


def validate_card_payload(report_date: str, card: dict):
    if not isinstance(card, dict):
        append_log(report_date, '发送失败：card 不是 dict')
        raise ValueError('发送失败：card 必须是飞书 interactive card 结构(dict)')
    if card.get('schema') != '2.0':
        append_log(report_date, f"发送失败：card.schema 非法：{card.get('schema')}")
        raise ValueError('发送失败：card.schema 必须为 2.0')
    header = card.get('header')
    if not isinstance(header, dict) or not isinstance(header.get('title'), dict):
        append_log(report_date, '发送失败：card.header/title 缺失')
        raise ValueError('发送失败：card.header/title 缺失')
    body = card.get('body')
    elements = body.get('elements') if isinstance(body, dict) else None
    if not isinstance(elements, list) or not elements:
        append_log(report_date, '发送失败：card.body.elements 缺失或为空')
        raise ValueError('发送失败：card.body.elements 缺失或为空')
    has_action = any(isinstance(el, dict) and el.get('tag') == 'action' for el in elements)
    if not has_action:
        append_log(report_date, '发送失败：card 缺少 action 按钮区')
        raise ValueError('发送失败：card 缺少 action 按钮区')


def ensure_card_only_command(report_date: str, cmd: list[str]):
    joined = ' '.join(cmd)
    if '--card' not in cmd:
        append_log(report_date, f'发送失败：命令未携带 --card：{joined}')
        raise ValueError('发送失败：未检测到原生卡片参数 --card，禁止发送')
    forbidden_flags = {'--message', '--text', '--markdown', '--md', '--presentation'}
    bad = [flag for flag in forbidden_flags if flag in cmd]
    if bad:
        append_log(report_date, f'发送失败：检测到非原生卡片参数 {bad}：{joined}')
        raise ValueError(f'发送失败：检测到非原生卡片发送参数 {bad}，禁止发送')


def send_card(report_date: str, card: dict, dry_run: bool):
    payload = {
        "action": "send",
        "channel": "feishu",
        "target": TARGET,
        "card": card,
    }

    if 'message' in payload or 'text' in payload or 'markdown' in payload or 'presentation' in payload:
        append_log(report_date, '发送失败：payload 出现普通文本或通用 presentation 字段')
        raise ValueError('发送失败：payload 出现普通文本或通用 presentation 字段，禁止发送')

    if payload["target"] != TARGET or not payload["target"].startswith("user:"):
        append_log(report_date, f'发送失败：目标非法，必须且只能是 {TARGET}')
        raise ValueError(f"发送目标非法，必须且只能是馨姐个人飞书: {TARGET}")

    validate_card_payload(report_date, card)

    append_log(report_date, STRICT_TEXT)
    append_log(report_date, f'开始发送飞书原生 interactive card，目标={TARGET}，dry_run={str(dry_run).lower()}')
    print(json.dumps(payload, ensure_ascii=False, indent=2))

    cmd = [
        "openclaw", "message", "send",
        "--channel", "feishu",
        "--target", TARGET,
        "--card", json.dumps(card, ensure_ascii=False),
    ]

    ensure_card_only_command(report_date, cmd)

    if dry_run:
        cmd.append("--dry-run")

    append_log(report_date, '发送前自检通过：仅最终资讯、仅原生 interactive card、仅个人飞书目标')
    result = subprocess.run(cmd, capture_output=True, text=True, check=False, cwd=str(BASE_DIR))
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

    append_log(report_date, '发送完成（卡片路径）')
    return 0


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--date', required=True, help='行业资讯日期 YYYY-MM-DD')
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()

    _, items = load_items(args.date)
    card = build_feishu_card(args.date, items)
    return send_card(args.date, card, args.dry_run)


if __name__ == '__main__':
    raise SystemExit(main())
