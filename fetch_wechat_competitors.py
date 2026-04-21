#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成友商公众号跟踪数据（T-7）

数据原则：
- 只保留真实可公开验证的内容
- 不捏造阅读量/点赞量等拿不到的数据
- 当前优先汇总品牌官方公众号/官方号在近7天公开发布的内容
- 数据输出到 docs/data/wechat/YYYY-MM-DD.json

当前跟踪品牌：蔚来 / 小鹏汽车 / 极氪
"""

import json
import os
import re
import subprocess
import sys
from datetime import datetime, timedelta, date
from urllib.parse import urlparse

ROOT = "/workspace/sentiment-dashboard"
OUT_DIR = os.path.join(ROOT, "docs/data/wechat")

BRANDS = [
    {
        "brand": "蔚来",
        "account": "蔚来",
        "queries": [
            "蔚来 公众号 近7天",
            "蔚来 微信公众号 发布 2026",
            "site:mp.weixin.qq.com 蔚来 微信公众号",
            "site:mp.weixin.qq.com NIO 蔚来"
        ]
    },
    {
        "brand": "小鹏汽车",
        "account": "小鹏汽车",
        "queries": [
            "小鹏汽车 公众号 近7天",
            "小鹏汽车 微信公众号 发布 2026",
            "site:mp.weixin.qq.com 小鹏汽车 微信公众号",
            "site:mp.weixin.qq.com XPENG 小鹏汽车"
        ]
    },
    {
        "brand": "极氪",
        "account": "极氪ZEEKR",
        "queries": [
            "极氪 公众号 近7天",
            "极氪 微信公众号 发布 2026",
            "site:mp.weixin.qq.com 极氪 微信公众号",
            "site:mp.weixin.qq.com ZEEKR 极氪"
        ]
    }
]


def run_web_search(query, count=8):
    cmd = [
        "python3", "-c",
        (
            "import json,sys;"
            "sys.path.insert(0,'/workspace/openclaw');"
            "print('')"
        )
    ]
    # 直接走 openclaw exec 外壳中的 web_search 不现实；这里改为调用 openclaw session 外部不可用。
    # 所以本脚本仅作为数据结构与去重整理器，真正搜索应由 Agent 调用 web_search 后写入。
    return []


def normalize_date(text):
    if not text:
        return ""
    m = re.search(r"(20\d{2})[-/.年](\d{1,2})[-/.月](\d{1,2})", text)
    if m:
        y, mo, d = m.groups()
        return f"{y}-{int(mo):02d}-{int(d):02d}"
    m2 = re.search(r"(\d{1,2})[-/.月](\d{1,2})", text)
    if m2:
        mo, d = m2.groups()
        y = date.today().year
        return f"{y}-{int(mo):02d}-{int(d):02d}"
    return ""


def in_t7(day_str, today):
    if not day_str:
        return False
    try:
        dt = datetime.strptime(day_str, "%Y-%m-%d").date()
    except Exception:
        return False
    return today - timedelta(days=7) <= dt <= today


def domain_label(url):
    try:
        host = urlparse(url).netloc.lower()
    except Exception:
        return ""
    if "mp.weixin.qq.com" in host:
        return "微信公众号"
    if "weixin.qq.com" in host:
        return "微信"
    return host or "网页"


def build_from_agent_results(raw_results, target_date):
    today = datetime.strptime(target_date, "%Y-%m-%d").date()
    brands = []
    for brand in raw_results:
        items = []
        seen = set()
        for item in brand.get("items", []):
            title = (item.get("title") or "").strip()
            url = (item.get("url") or "").strip()
            desc = (item.get("desc") or item.get("snippet") or "").strip()
            publish_date = (item.get("publish_date") or "").strip()
            if not publish_date:
                publish_date = normalize_date(desc) or normalize_date(title)
            if not title or not url:
                continue
            if not in_t7(publish_date, today):
                continue
            key = url
            if key in seen:
                continue
            seen.add(key)
            items.append({
                "title": title,
                "url": url,
                "desc": desc[:180],
                "publish_date": publish_date,
                "source": item.get("source") or domain_label(url)
            })
        items.sort(key=lambda x: (x.get("publish_date", ""), x.get("title", "")), reverse=True)
        brands.append({
            "brand": brand.get("brand", ""),
            "account": brand.get("account", ""),
            "items": items
        })
    return {
        "target_date": target_date,
        "window": "T-7",
        "brands": brands,
        "sources_note": "仅收录近7天内可公开验证的官方公众号/官方号相关内容；不展示无法核实的阅读量、点赞等字段。"
    }


def save_payload(payload):
    os.makedirs(OUT_DIR, exist_ok=True)
    target_date = payload["target_date"]
    out = os.path.join(OUT_DIR, f"{target_date}.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    dates_path = os.path.join(OUT_DIR, "dates.json")
    dates = []
    if os.path.exists(dates_path):
        try:
            dates = json.load(open(dates_path, "r", encoding="utf-8"))
        except Exception:
            dates = []
    if target_date not in dates:
        dates.append(target_date)
    dates = sorted(set(dates))
    with open(dates_path, "w", encoding="utf-8") as f:
        json.dump(dates, f, ensure_ascii=False, indent=2)
    return out


def main():
    if len(sys.argv) < 2:
        print("usage: fetch_wechat_competitors.py <raw-json-path|-> [target_date]")
        sys.exit(1)
    raw_path = sys.argv[1]
    target_date = sys.argv[2] if len(sys.argv) > 2 else date.today().strftime("%Y-%m-%d")
    if raw_path == "-":
        raw = json.load(sys.stdin)
    else:
        raw = json.load(open(raw_path, "r", encoding="utf-8"))
    payload = build_from_agent_results(raw, target_date)
    out = save_payload(payload)
    total = sum(len(b.get("items", [])) for b in payload.get("brands", []))
    print(json.dumps({"ok": True, "out": out, "total": total}, ensure_ascii=False))


if __name__ == "__main__":
    main()
