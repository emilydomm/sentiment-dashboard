#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智能电动行业资讯抓取脚本
每天通过 web_search 抓取最新汽车行业动态
关键词：底盘、电池、电机、增程、充电、三电、能耗、悬架
"""
import json
import os
import sys
from datetime import date, datetime

# 添加 OpenClaw tools 路径（如果需要直接调用）
# 注意：这个脚本需要在 OpenClaw 环境中通过 Agent 调用 web_search 工具

# 行业资讯关键词
KEYWORDS = ['底盘', '电池', '电机', '增程', '充电', '三电', '能耗', '悬架']

def parse_search_results(keyword, search_results):
    """
    解析 web_search 返回的结果
    search_results 格式: [{"title": ..., "url": ..., "snippet": ..., "publishedDate": ...}, ...]
    """
    items = []
    for result in search_results:
        title = result.get('title', '')
        url = result.get('url', '')
        snippet = result.get('snippet', '')
        published = result.get('publishedDate', '') or result.get('date', '')
        
        # 清理摘要
        desc = snippet[:200] + '…' if len(snippet) > 200 else snippet
        
        # 简单判断情感（行业资讯大多为中性）
        sentiment = 'neutral'
        if any(w in title + snippet for w in ['突破', '创新', '领先', '全球首', '量产', '发布']):
            sentiment = 'positive'
        elif any(w in title + snippet for w in ['召回', '故障', '投诉', '问题', '下滑']):
            sentiment = 'negative'
        
        items.append({
            'platform': 'web',
            'note_id': url,  # 用 URL 作为唯一标识
            'title': title,
            'desc': desc,
            'author': '行业资讯',
            'ip_location': '',
            'liked_count': 0,
            'comment_count': 0,
            'share_count': 0,
            'publish_date': published or date.today().strftime('%Y-%m-%d'),
            'url': url,
            'sentiment': sentiment,
            'keyword': keyword  # 标记来源关键词
        })
    
    return items


def generate_placeholder_structure():
    """
    生成占位数据结构（空列表），供 Agent 填充真实数据
    返回格式：{keyword: [items], ...}
    """
    return {kw: [] for kw in KEYWORDS}


if __name__ == '__main__':
    """
    ⚠️ 此脚本不能直接运行，需要通过 OpenClaw Agent 调用 web_search 工具
    
    Agent 调用示例：
    1. 读取本脚本了解数据结构
    2. 对每个关键词调用 web_search(query=kw, count=3)
    3. 用 parse_search_results() 处理结果
    4. 合并所有结果并保存到 docs/data/industry/YYYY-MM-DD.json
    """
    today_str = date.today().strftime('%Y-%m-%d')
    print(f"📅 目标日期: {today_str}")
    print(f"🔍 关键词列表: {', '.join(KEYWORDS)}")
    print(f"")
    print(f"⚠️  此脚本需要 OpenClaw Agent 调用 web_search 工具执行")
    print(f"请在 Agent 中运行以下流程：")
    print(f"")
    print(f"for keyword in {KEYWORDS}:")
    print(f"    results = web_search(query=keyword + ' 新能源汽车', count=3)")
    print(f"    items.extend(parse_search_results(keyword, results))")
    print(f"")
    print(f"最终保存到: /workspace/sentiment-dashboard/docs/data/industry/{today_str}.json")
