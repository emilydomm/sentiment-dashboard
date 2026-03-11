#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
每日舆情数据生成脚本
逻辑：抓取小红书最新内容，只保留T-1（昨天）发布的帖子
情感判断：优先读正文(desc)，标题仅做辅助参考
"""
import json, glob, os, re
from datetime import date, datetime, timedelta

def clean_desc(text):
    """清理摘要：去掉话题标签和@"""
    text = re.sub(r'#[^#\[]*(\[话题\])?#?', '', text or '')
    text = re.sub(r'@\S+', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text[:150] + '…' if len(text) > 150 else text

def judge_sentiment(title, desc):
    """
    情感判断：优先看正文内容，再看标题
    正向关键词：体验好、方便、快、推荐等
    负向关键词：排队、故障、占用、太差等
    负向但实际正向的情况：标题含"焦虑"但正文是说没焦虑/解决了焦虑
    """
    text = (desc or '') + ' ' + (title or '')
    
    # 正向信号（强）
    pos_strong = ['体验很棒', '体验不错', '很好用', '推荐', '方便', '秒充', '10分钟', 
                  '没有焦虑', '无焦虑', '解决了', '圈粉', '真香', '太爽', '好评',
                  '不用排队', '来就充', '随时充', '体验还是很棒', '体验还是很好']
    
    # 负向信号（强）
    neg_strong = ['排队等', '排了很久', '排队半小时', '排队1小时', '等位', '充不上',
                  '故障', '坏了', '损坏', '占位', '霸占', '投诉', '太贵了', '收费不合理',
                  '服务差', '体验差', '太差', '失望', '坑']
    
    # 标题中的误判词（出现在标题但实际内容可能是正向）
    misleading_neg_in_title = ['焦虑', '伪命题', '悲剧']
    
    text_lower = text.lower()
    
    # 优先检查强正向
    if any(w in text for w in pos_strong):
        return 'positive'
    
    # 优先检查强负向
    if any(w in text for w in neg_strong):
        return 'negative'
    
    # 标题含误导词，但正文有正向内容时，判为正向
    title_has_misleading = any(w in (title or '') for w in misleading_neg_in_title)
    desc_has_positive = any(w in (desc or '') for w in ['很棒', '不错', '好', '快', '方便', '推荐', '赞'])
    if title_has_misleading and desc_has_positive:
        return 'positive'
    
    # 一般负向词（仅在标题）
    neg_title = ['伪命题', '悲剧', '崩塌', '失败', '差评', '质疑', '问题多']
    if any(w in (title or '') for w in neg_title):
        return 'negative'
    
    return 'neutral'


def generate(target_date_str=None):
    """
    生成指定日期的舆情数据
    target_date_str: 目标日期字符串 YYYY-MM-DD，默认为昨天
    爬虫文件应当是今天刚跑的最新文件
    """
    if target_date_str is None:
        target_date_str = (date.today() - timedelta(days=1)).strftime('%Y-%m-%d')
    
    today_str = date.today().strftime('%Y-%m-%d')
    print(f"生成 {today_str} 的舆情报告（数据范围：{target_date_str}）")
    
    # 读取最新爬虫结果
    files = sorted(
        glob.glob('/workspace/MediaCrawler/data/xhs/json/search_contents_*.json'),
        key=os.path.getmtime, reverse=True
    )
    
    output = []
    
    if files:
        data = json.load(open(files[0]))
        seen = set()
        notes = [n for n in data if n.get('note_id','') not in seen and not seen.add(n.get('note_id',''))]
        
        # ⭐ 关键：只保留昨天（T-1）发布的内容
        filtered_notes = []
        for n in notes:
            ts = int(n.get('time', 0) or 0)
            if ts == 0:
                continue
            pub_date = datetime.fromtimestamp(ts / 1000).strftime('%Y-%m-%d')
            if pub_date == target_date_str:
                filtered_notes.append((pub_date, n))
        
        # 如果昨天完全没有新内容，放宽到近7天
        if not filtered_notes:
            print(f"⚠️  {target_date_str} 无新内容，放宽到近7天")
            cutoff = (datetime.strptime(target_date_str, '%Y-%m-%d') - timedelta(days=6)).strftime('%Y-%m-%d')
            for n in notes:
                ts = int(n.get('time', 0) or 0)
                if ts == 0:
                    continue
                pub_date = datetime.fromtimestamp(ts / 1000).strftime('%Y-%m-%d')
                if pub_date >= cutoff:
                    filtered_notes.append((pub_date, n))
        
        # 按热度排序
        filtered_notes.sort(
            key=lambda x: int(x[1].get('liked_count', 0) or 0) + int(x[1].get('comment_count', 0) or 0),
            reverse=True
        )
        
        for pub_date, n in filtered_notes:
            title = n.get('title', '')
            desc = clean_desc(n.get('desc', ''))
            sentiment = judge_sentiment(title, desc)
            output.append({
                'platform': 'xhs',
                'note_id': n.get('note_id', ''),
                'title': title,
                'desc': desc,
                'author': n.get('nickname', ''),
                'ip_location': n.get('ip_location', ''),
                'liked_count': int(n.get('liked_count', 0) or 0),
                'comment_count': int(n.get('comment_count', 0) or 0),
                'share_count': int(n.get('share_count', 0) or 0),
                'publish_date': pub_date,
                'url': f'https://www.xiaohongshu.com/explore/{n.get("note_id", "")}',
                'sentiment': sentiment
            })
        
        print(f"小红书: {len(output)} 条（T-1: {target_date_str}）")
    
    return output, today_str


if __name__ == '__main__':
    import sys
    target = sys.argv[1] if len(sys.argv) > 1 else None
    output, report_date = generate(target)
    
    os.makedirs('/workspace/sentiment-dashboard/docs/data', exist_ok=True)
    out_path = f'/workspace/sentiment-dashboard/docs/data/{report_date}.json'
    json.dump(output, open(out_path, 'w'), ensure_ascii=False, indent=2)
    
    # 更新日期索引
    dates = sorted([
        os.path.basename(f).replace('.json', '')
        for f in glob.glob('/workspace/sentiment-dashboard/docs/data/*.json')
        if re.match(r'\d{4}-\d{2}-\d{2}', os.path.basename(f))
    ])
    json.dump(dates, open('/workspace/sentiment-dashboard/docs/data/dates.json', 'w'))
    
    pos = [x for x in output if x['sentiment'] == 'positive']
    neg = [x for x in output if x['sentiment'] == 'negative']
    neu = [x for x in output if x['sentiment'] == 'neutral']
    print(f"✅ 生成完成: {report_date}.json | 共{len(output)}条 | 正向{len(pos)} 负向{len(neg)} 中性{len(neu)}")
