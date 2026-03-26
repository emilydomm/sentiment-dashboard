#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从文章URL提取og:image配图
被行业资讯生成流程调用，对已有JSON数据补充image字段
用法: python3 fetch_image.py docs/data/industry/2026-03-26.json
"""
import urllib.request, re, json, sys, time, os

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 11; Pixel 5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml',
    'Accept-Language': 'zh-CN,zh;q=0.9',
}

# 无意义图片的特征关键词（路径或文件名含这些词的一律过滤）
BAD_IMAGE_PATTERNS = [
    'logo', 'icon', 'avatar', 'placeholder', 'default', 'sprite', 'blank',
    'searchbox',  # bdstatic searchbox目录下基本都是logo
    '/gcp/',      # bdstatic gcp路径多为品牌logo
    'qrcode', 'qr_code',
    'watermark',
    '/brand/',
    'favicon',
]

def is_valid_image(url):
    """判断图片URL是否为有效内容图（非logo/icon）"""
    url_lower = url.lower()
    if not url.startswith('http'):
        return False
    if any(p in url_lower for p in BAD_IMAGE_PATTERNS):
        return False
    return True

def fetch_og_image(url, timeout=6):
    """从URL提取og:image，失败返回空字符串"""
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        html = urllib.request.urlopen(req, timeout=timeout).read().decode('utf-8', errors='ignore')
        
        patterns = [
            r'<meta[^>]+property=["\']og:image["\'][^>]+content=["\']([^"\']+)["\']',
            r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+property=["\']og:image["\']',
            r'<meta[^>]+name=["\']twitter:image["\'][^>]+content=["\']([^"\']+)["\']',
            r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+name=["\']twitter:image["\']',
        ]
        for p in patterns:
            m = re.search(p, html, re.I | re.S)
            if m:
                img = m.group(1).strip()
                if img.startswith('//'):
                    img = 'https:' + img
                if is_valid_image(img):
                    return img
        
        # 兜底：找第一张内容大图
        img_tags = re.findall(r'<img[^>]+src=["\']([^"\']{50,})["\']', html, re.I)
        for img in img_tags:
            if any(ext in img.lower() for ext in ['.jpg','.jpeg','.png','.webp']):
                if is_valid_image(img):
                    return img
    except:
        pass
    return ""


def enrich_images(json_file):
    """为JSON文件中无配图的条目补充image字段"""
    data = json.load(open(json_file))
    updated = 0
    for item in data:
        if not item.get('image'):
            img = fetch_og_image(item.get('url', ''))
            if img:
                item['image'] = img
                updated += 1
            time.sleep(0.4)  # 避免请求过快
    
    json.dump(data, open(json_file, 'w'), ensure_ascii=False, indent=2)
    has_img = sum(1 for i in data if i.get('image'))
    print(f"配图补充完成: {updated}条新增, 共{has_img}/{len(data)}条有图")
    return updated


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("用法: python3 fetch_image.py <json_file>")
        sys.exit(1)
    enrich_images(sys.argv[1])
