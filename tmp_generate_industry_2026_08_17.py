import requests, xml.etree.ElementTree as ET, html, re, json, os
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from bs4 import BeautifulSoup

report_date = '2026-08-17'
cutoff = datetime(2026, 8, 10, tzinfo=timezone.utc)
queries = [
    ('电池技术','新能源汽车 电池 after:2026-08-10 before:2026-08-18'),
    ('底盘技术','新能源汽车 底盘 after:2026-08-10 before:2026-08-18'),
    ('充电技术','新能源汽车 充电 after:2026-08-10 before:2026-08-18'),
    ('智能驾驶','新能源汽车 智能驾驶 after:2026-08-10 before:2026-08-18'),
    ('新车发布','新能源汽车 新车 发布 after:2026-08-10 before:2026-08-18'),
]
headers = {'User-Agent': 'Mozilla/5.0'}
valid = []
seen = set()

def clean(s):
    s = (s or '').replace('“', '"').replace('”', '"').replace('‘', "'").replace('’', "'")
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
        r = requests.get(url, headers=headers, timeout=12)
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
    try:
        text = requests.get(rss, headers=headers, timeout=20).text
        root = ET.fromstring(text)
    except Exception as e:\n        print('RSS ERROR', keyword, e)\n        continue\n    for it in root.findall('./channel/item')[:12]:
        title = html.unescape(it.findtext('title', '')).strip()
        title = re.sub(r'\s*-\s*[^-]+$', '', title)
        try:
            pub = parsedate_to_datetime(it.findtext('pubDate')).astimezone(timezone.utc)
        except Exception:
            continue
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
            'desc': clean(desc),
            'image': ''
        }
        if len(item['desc']) < 20:
            continue
        valid.append(item)

preferred_hosts = ['news.qq.com','news.cn','people.com.cn','ithome.com','autohome.com.cn','thecover.cn','zjnews.com.cn','cnev.cn','itbear.com.cn','byd.com','bydglobal.com']
valid.sort(key=lambda x: (x['publish_date'], sum(h in x['url'] for h in preferred_hosts)), reverse=True)

result = []
used_kw = {}
for item in valid:
    if any(x['url'] == item['url'] for x in result):
        continue
    if used_kw.get(item['keyword'], 0) >= 2:
        continue
    result.append(item)
    used_kw[item['keyword']] = used_kw.get(item['keyword'], 0) + 1
    if len(result) == 8:
        break

path = '/workspace/sentiment-dashboard/docs/data/industry/2026-08-17.json'
os.makedirs(os.path.dirname(path), exist_ok=True)
raw = json.dumps(result, ensure_ascii=False, indent=2)
json.loads(raw)
open(path, 'w', encoding='utf-8').write(raw)
print(raw)
