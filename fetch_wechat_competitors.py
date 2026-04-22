#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成友商公众号跟踪数据（T-7）

数据原则：
- 只保留真实可公开验证的内容
- 不捏造阅读量/点赞量等拿不到的数据
- 只收录品牌官方公众号原文 `mp.weixin.qq.com` 链接
- 官网页、转载页、聚合页一律不收录
- 数据输出到 docs/data/wechat/YYYY-MM-DD.json

当前跟踪品牌：蔚来 / 小鹏汽车 / 极氪

实现策略（当前可达到的最稳方案）：
1. 允许接收外部检索/人工确认得到的原文直链
2. 对原文链接做规范化去重
3. 只保留 T-7 范围内条目
4. 不再把“公开搜索没搜到”误写成“品牌没有发文”

说明：
- 微信原文公开搜索召回极不稳定，无法仅靠通用 search 保证“全量发现”。
- 因此本脚本的职责调整为：
  **严谨收录已确认的官方原文**，而不是基于弱召回搜索结果输出假性“0条/全量”。
"""

import json
import os
import re
import sys
from datetime import datetime, timedelta, date
from urllib.parse import urlparse, parse_qs

ROOT = "/workspace/sentiment-dashboard"
OUT_DIR = os.path.join(ROOT, "docs/data/wechat")

BRANDS = [
    {
        "brand": "蔚来",
        "account": "蔚来",
        "queries": [
            "site:mp.weixin.qq.com 蔚来 微信公众号 原文",
            "site:mp.weixin.qq.com NIO 蔚来 原文",
        ]
    },
    {
        "brand": "小鹏汽车",
        "account": "小鹏汽车",
        "queries": [
            "site:mp.weixin.qq.com 小鹏汽车 微信公众号 原文",
            "site:mp.weixin.qq.com XPENG 小鹏汽车 原文",
        ]
    },
    {
        "brand": "极氪",
        "account": "极氪ZEEKR",
        "queries": [
            "site:mp.weixin.qq.com 极氪 微信公众号 原文",
            "site:mp.weixin.qq.com ZEEKR 极氪 原文",
        ]
    }
]


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
        return "微信公众号原文"
    return host or "网页"


def canonical_mp_url(url):
    url = (url or "").strip()
    if not url:
        return ""
    try:
        u = urlparse(url)
        if "mp.weixin.qq.com" not in u.netloc.lower():
            return ""
        qs = parse_qs(u.query)
        if u.path.startswith("/s"):
            biz = qs.get("__biz", [""])[-1]
            mid = qs.get("mid", [""])[-1]
            idx = qs.get("idx", [""])[-1]
            sn = qs.get("sn", [""])[-1]
            if biz and mid and idx and sn:
                return f"https://mp.weixin.qq.com/s?__biz={biz}&mid={mid}&idx={idx}&sn={sn}"
            return f"https://mp.weixin.qq.com{u.path}"
        return f"https://mp.weixin.qq.com{u.path}"
    except Exception:
        return url


def normalize_item(item):
    title = (item.get("title") or "").strip()
    url = canonical_mp_url((item.get("url") or "").strip())
    desc = (item.get("desc") or item.get("snippet") or "").strip()
    publish_date = (item.get("publish_date") or "").strip()
    if not publish_date:
        publish_date = normalize_date(desc) or normalize_date(title)
    source = (item.get("source") or "").strip() or domain_label(url)
    return {
        "title": title,
        "url": url,
        "desc": desc[:180],
        "publish_date": publish_date,
        "source": source,
    }


def collect_candidates(brand):
    out = []
    for key in ("items", "manual_items", "confirmed_items", "extra_items"):
        val = brand.get(key)
        if isinstance(val, list):
            out.extend(val)
    return out


def build_sources_note(total):
    if total == 0:
        return (
            "当前页仅展示已确认的品牌官方公众号原文 mp.weixin.qq.com 链接。"
            "由于微信原文公开检索召回不稳定，‘未展示’不等于‘品牌近7天未发文’，"
            "只表示当前自动链路尚未确认到可入库的官方原文直链。"
        )
    return (
        "仅收录近7天内可公开验证的品牌官方公众号原文 mp.weixin.qq.com 链接；"
        "官网页、转载页、聚合页均不展示，不展示无法核实的阅读量、点赞等字段。"
        "由于微信原文公开检索召回不稳定，当前结果代表‘已确认收录’，不承诺纯靠通用搜索即可全量发现。"
    )


def build_from_agent_results(raw_results, target_date):
    today = datetime.strptime(target_date, "%Y-%m-%d").date()
    brands = []
    total = 0
    for brand in raw_results:
        items = []
        seen = set()
        for item in collect_candidates(brand):
            row = normalize_item(item)
            title = row["title"]
            url = row["url"]
            publish_date = row["publish_date"]
            if not title or not url:
                continue
            parsed_host = urlparse(url).netloc.lower()
            if "mp.weixin.qq.com" not in parsed_host:
                continue
            if not publish_date:
                continue
            if not in_t7(publish_date, today):
                continue
            key = url
            if key in seen:
                continue
            seen.add(key)
            items.append(row)
        items.sort(key=lambda x: (x.get("publish_date", ""), x.get("title", ""), x.get("url", "")), reverse=True)
        total += len(items)
        brands.append({
            "brand": brand.get("brand", ""),
            "account": brand.get("account", ""),
            "items": items
        })
    return {
        "target_date": target_date,
        "window": "T-7",
        "brands": brands,
        "sources_note": build_sources_note(total)
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
