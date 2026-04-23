#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智能电动行业资讯抓取规则说明

这个文件不直接执行抓取，而是给定时任务 / Agent 提供“怎么查、怎么收、怎么拒绝”的规则。
重点修复：避免把“车展前夕 / 媒体之夜 / 发布会当天”的有效资讯漏掉。
"""
import json
from datetime import date, datetime, timedelta

# 基础关键词
KEYWORDS = ['底盘', '电池', '电机', '增程', '充电', '三电', '能耗', '悬架']

# 事件补查关键词：当车展 / 发布会密集期必须额外搜索，不能只靠基础词
EVENT_KEYWORDS = [
    '北京车展', '上海车展', '车展前夕', '媒体之夜', '品牌之夜',
    '发布会', '上市', '首发', '亮相', '探馆', '技术发布会'
]

# 高优先级技术词：用于和事件词组合，优先补查技术密度更高的内容
TECH_HOTWORDS = [
    '800V', '900V', '6C超充', '兆瓦超充', '钠离子电池', '固态电池',
    '空气悬架', '后轮转向', '线控底盘', '智能体AI', 'L3', '辅助驾驶'
]

# 推荐来源（不是硬编码白名单，但应优先采用）
PREFERRED_SOURCES = [
    '央视网', '新华社', '人民日报', '新京报', '财联社', '澎湃新闻',
    'IT之家', '易车', '汽车之家', '懂车帝', '官方新闻中心', '品牌官网'
]


def in_t7_window(publish_date_str, today_str=None):
    """严格按文章发布日期判断是否在 T-7 窗口内。"""
    if not publish_date_str:
        return False
    if today_str is None:
        today = date.today()
    else:
        today = datetime.strptime(today_str, '%Y-%m-%d').date()
    try:
        pub = datetime.strptime(publish_date_str, '%Y-%m-%d').date()
    except ValueError:
        return False
    start = today - timedelta(days=7)
    return start <= pub <= today


def build_search_plan(today_str=None):
    """
    给 Agent 的检索计划：
    1. 先跑基础关键词；
    2. 再跑事件补查；
    3. 事件期一定补“车展 / 发布会 / 媒体之夜 / 探馆 / 首发 / 上市”。
    """
    if today_str is None:
        today_str = date.today().strftime('%Y-%m-%d')

    base_queries = [
        f'{kw} 新能源汽车 {today_str}' for kw in KEYWORDS
    ]

    event_queries = [
        f'{event} 新能源汽车 {today_str}' for event in EVENT_KEYWORDS
    ]

    tech_event_queries = [
        f'{event} {tech} {today_str}'
        for event in ['北京车展', '媒体之夜', '发布会', '上市', '首发', '探馆']
        for tech in TECH_HOTWORDS
    ]

    return {
        'base_queries': base_queries,
        'event_queries': event_queries,
        'tech_event_queries': tech_event_queries,
    }


def inclusion_rules():
    """返回给 Agent 的明确收录规则。"""
    return [
        '只按文章发布日期做 T-7 过滤，不能用活动举办日替代文章发布日期。',
        '车展前夕、媒体之夜、发布会当天/次日，如有正式报道，必须重点补查。',
        '优先收录含明确技术信息的内容，如电池、超充、底盘、智能驾驶、电气架构。',
        '前瞻/盘点类文章只有在发布时间合规且信息密度高、包含明确新技术/新车型实质信息时才可收录。',
        '若搜索结果只显示活动日期，无法确认文章发布日期，则拒绝收录。',
        '若条目与当天已有资讯高度重复，应去重，保留信息量更高、来源更可靠的一条。',
        '宁可少，也不能收录发布日期不实或无法核验的内容。',
    ]


def fallback_checklist():
    """当首轮检索结果过少时，强制执行的补查清单。"""
    return [
        '检查当天/前一日是否有大型车展、品牌之夜、技术发布会、媒体之夜。',
        '检查头部电池企业、电驱企业、主机厂是否发布技术稿或上市稿。',
        '检查车展探馆/首发/上市类稿件，优先选择带参数、架构、补能、底盘、智驾信息的报道。',
        '如果首轮结果为0条，不能直接结束，必须执行事件补查和技术词补查后再下结论。',
    ]


if __name__ == '__main__':
    today_str = date.today().strftime('%Y-%m-%d')
    print('📅 目标日期:', today_str)
    print('🔍 基础关键词:', ', '.join(KEYWORDS))
    print('📍 事件补查关键词:', ', '.join(EVENT_KEYWORDS))
    print('⚙️ 技术热点词:', ', '.join(TECH_HOTWORDS))
    print('\n【收录规则】')
    for idx, rule in enumerate(inclusion_rules(), 1):
        print(f'{idx}. {rule}')
    print('\n【首轮不足时必须补查】')
    for idx, rule in enumerate(fallback_checklist(), 1):
        print(f'{idx}. {rule}')
    print('\n【建议查询计划】')
    plan = build_search_plan(today_str)
    print(json.dumps(plan, ensure_ascii=False, indent=2))
