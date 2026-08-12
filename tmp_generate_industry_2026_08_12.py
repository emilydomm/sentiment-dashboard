import requests, xml.etree.ElementTree as ET, html, re, json
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from bs4 import BeautifulSoup
import os

queries = [
    ('电池技术','新能源汽车 电池 after:2026-08-05 before:2026-08-13'),
    ('底盘技术','新能源汽车 底盘 after:2026-08-05 before:2026-08-13'),
    ('充电技术','新能源汽车 充电 after:2026-08-05 before:2026-08-13'),
    ('智能驾驶','新能源汽车 智能驾驶 after:2026-08-05 before:2026-08-13'),
    ('新车发布','新能源汽车 新车 发布 after:2026-08-05 before:2026-08-13'),
]
headers = {'User-Agent': 'Mozilla/5.0'}
cutoff = datetime(2026, 8, 5, tzinfo=timezone.utc)
valid = []
seen = set()

def clean(s):
    s = s.replace('“', '"').replace('”', '"').replace('‘', "'").replace('’', "'")
    s = re.sub(r'\s+', ' ', s).strip()
    return s

def resolve_google(link):
    try:
        r = requests.get(link, headers=headers, timeout=20, allow_redirects=True)
        return r.url
    except Exception:
        return link

def fetch_desc(url):
    try:
        r = requests.get(url, headers=headers, timeout=8)
        soup = BeautifulSoup(r.text, 'html.parser')
        txt = ''
        for key in ['og:description', 'description']:
            tag = soup.find('meta', attrs={'property': key}) or soup.find('meta', attrs={'name': key})
            if tag and tag.get('content'):
                txt = tag['content']
                break
        if not txt:
            ps = [p.get_text(' ', strip=True) for p in soup.find_all('p')[:20]]
            txt = ' '.join([p for p in ps if len(p) > 20][:2])
        return clean(txt)[:140]
    except Exception:
        return ''

for keyword, q in queries:
    rss = 'https://news.google.com/rss/search?q=' + requests.utils.quote(q) + '&hl=zh-CN&gl=CN&ceid=CN:zh-Hans'
    text = requests.get(rss, headers=headers, timeout=20).text
    root = ET.fromstring(text)
    for it in root.findall('./channel/item')[:8]:
        title = html.unescape(it.findtext('title', '')).strip()
        title = re.sub(r'\s*-\s*[^-]+$', '', title)
        pub = parsedate_to_datetime(it.findtext('pubDate')).astimezone(timezone.utc)
        if pub < cutoff:
            continue
        url = resolve_google(it.findtext('link', ''))
        if 'news.google.com' in url:
            continue
        key = (title, url)
        if key in seen:
            continue
        seen.add(key)
        desc = fetch_desc(url)
        item = {
            'title': clean(title),
            'url': url,
            'publish_date': pub.date().isoformat(),
            'keyword': keyword,
            'desc': desc,
            'image': ''
        }
        if len(item['desc']) < 20:
            continue
        valid.append(item)

preferred = []
for host_kw in [
    ('news.cn', '智能驾驶'),
    ('news.cn', '充电技术'),
    ('news.cn', '新车发布'),
    ('people.com.cn', '充电技术'),
    ('thecover.cn', '智能驾驶'),
    ('zjnews.com.cn', '底盘技术'),
    ('ideacarbon.org', '充电技术'),
]:
    host, kw = host_kw
    for item in valid:
        if kw == item['keyword'] and host in item['url'] and item not in preferred:
            preferred.append(item)

for item in valid:
    if item not in preferred and item['keyword'] not in [x['keyword'] for x in preferred]:
        preferred.append(item)
for item in valid:
    if item not in preferred:
        preferred.append(item)

result = []
used_kw = {}
for item in preferred:
    if item['url'] in [x['url'] for x in result]:
        continue
    if used_kw.get(item['keyword'], 0) >= 2:
        continue
    result.append(item)
    used_kw[item['keyword']] = used_kw.get(item['keyword'], 0) + 1
    if len(result) == 8:
        break

out = result[:8]
path = 'docs/data/industry/2026-08-12.json'
os.makedirs(os.path.dirname(path), exist_ok=True)
raw = json.dumps(out, ensure_ascii=False, indent=2)
json.loads(raw)
open(path, 'w', encoding='utf-8').write(raw)
print(raw)
