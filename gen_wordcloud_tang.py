import jieba, re
import wordcloud as wc_module
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from collections import Counter
import numpy as np, sys, requests, time

sys.path.insert(0, '/workspace/openclaw/skills/feishu-doc-operations/scripts')
from feishu_doc_operations import FeishuDocOperations, obtainIdaasClientId, obtainIdaasClientSecret, obtainUserName

HOST = "https://cfe-feishu-server.chehejia.com"
FEISHU_APPID = "cli_a9bc3a82cef9dbd3"
SERVICE_ID = "35CWIoLZyI9uyZlJ6ASkAc"
SCOPES = ["doc:write","doc:read","default"]
USER_NAME = obtainUserName()
DOC_ID = "KL2adSmtSoOe8VxsXBqcK5den4e"
IMAGE_BLOCK_ID = "doxcnpZcb4TvID3yQnLWpyOKlhf"

COOKIE = "SINAGLOBAL=8306079426989.741.1736915993605; SCF=Ap2VIumoIlnzd8GYxqpPDuvlCY2dmCF67MZ96yKpBCttxVpPMrLVYKGj2r80eH4VWBJ1hp_279InrVSswbbglDA.; _s_tentry=weibo.com; Apache=9747779315771.492.1772256110766; ULV=1772256110768:9:2:1:9747779315771.492.1772256110766:1770618743894; UOR=,,li.feishu.cn; SUB=_2A25E4aiLDeRhGeRP6FIZ8SbLzjiIHXVnnqRDrDV8PUNbmtANLRDFkW9NUCtPvUwDcmAgX0vXqR5yHF8WJqVpiFuH; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWK9RW5sfDhg8exfWJYm9f45JpX5KzhUgL.Fozpe05ReKnNSKB2dJLoI0nLxK-L1KBL1K5LxKBLB.eLB-qLxKBLB.eLB-q_TCH8SC-4SF-4eFH8SC-RxF-RxCH8SCHWxb-RSBtt; ALF=02_1779262939"
wb_headers = {"Cookie": COOKIE, "User-Agent": "Mozilla/5.0 Chrome/120.0.0.0 Safari/537.36", "Referer": "https://weibo.com/"}
TANG_UID = "2130818754"

week_mblogids = [
    "QBGiFkecJ","QBEppizn9","QBxt4pAwy","QBvWt6TGU","QBubxsvg1","QBkYexUDu",
    "QBgLUFLkW","QBgFMCiYe","QBgkVo2n2","QBca3mQf6","QB6PU8XNy","QB5JmitI3",
    "QB2Y9kNI6","QB2UhsMW4","QB2TywLhn","QAXvUjSys","QAXvCvAir","QATxqhIFN",
    "QAO7N5ZEn","QANJW9HRu","QAMo286FM","QAKkQcycN","QAJWA9jrp","QAJV3zEXp",
    "QAIZ678j6",
]

all_comments = []
for mblogid in week_mblogids:
    resp = requests.get(f"https://weibo.com/ajax/statuses/show?id={mblogid}", headers=wb_headers)
    mid = resp.json().get('mid','')
    if not mid: time.sleep(0.15); continue
    try:
        cr = requests.get(
            f"https://weibo.com/ajax/statuses/buildComments?is_reload=1&id={mid}&is_show_bulletin=2&is_mix=0&count=20&uid={TANG_UID}&fetch_level=0&locale=zh-CN",
            headers=wb_headers)
        for c in cr.json().get('data', []):
            ct = re.sub(r'<[^>]+>', '', c.get('text','')).strip()
            ct = re.sub(r'http\S+', '', ct).strip()
            if len(ct) >= 5:
                all_comments.append(ct)
    except: pass
    time.sleep(0.18)

stopwords = set([
    '的','了','在','是','我','有','和','就','不','人','都','一','一个','上','也','很',
    '到','说','要','去','你','会','着','没有','看','好','这','来','他','用','们','为',
    '以','可以','但','这个','已经','对','吗','啊','吧','呢','嗯','哦','呀','啦','哇',
    '嘛','嗨','微博','超话','理想汽车','查看','图片','评论','转发','关注','点赞',
    '网页链接','视频','直播','链接','进行','名','等','个','时','后','中','于','与',
    '及','从','而','其','或','如','将','被','让','把','给','向','比','因','所以',
    '但是','然后','还是','什么','这样','那么','这么','其实','大家','我们','自己',
    '可能','应该','需要','知道','感觉','觉得','希望','还有','同时','而且','虽然',
    '因为','如果','回复','一下','不是','就是','其他','以后','这种','那个','来了',
    '非常','表示','发现','发布','开始','相关','方式','内容','活动','分享','明天',
    '推荐','今天','昨天','现在','时间','问题','情况','哈哈哈','哈哈','哈哈哈哈',
    '加油','支持','理想','汽车','唐博','伯伯','唐华寅','回复','唐伯伯',
    '抽奖','限定','春日','火爆','周五','上午','详情','流媒体','起来','为什么',
    '前备','吸引','地方','友谊','不能','不会','一次','特别','终于','明天',
])

words = jieba.cut(' '.join(all_comments))
filtered = [w.strip() for w in words
            if len(w.strip()) >= 2
            and w.strip() not in stopwords
            and not re.match(r'^[0-9a-zA-Z\s\W]+$', w.strip())]
freq = Counter(filtered)

# 自定义绿色系颜色函数：频次越高颜色越深
# 颜色范围：浅绿(#a8d5a2) -> 中绿(#4caf50) -> 深绿(#1b5e20)
max_freq = max(freq.values()) if freq else 1

def green_color_func(word, font_size, position, orientation, random_state=None, **kwargs):
    count = freq.get(word, 1)
    ratio = count / max_freq  # 0~1，频次越高越接近1
    # 深绿到浅绿的渐变：ratio=1 -> 深绿 #1a5c2a, ratio=0 -> 浅绿 #b7ddb0
    r = int(183 - ratio * (183 - 26))   # 183->26
    g = int(221 - ratio * (221 - 92))   # 221->92
    b = int(176 - ratio * (176 - 42))   # 176->42
    return f"rgb({r},{g},{b})"

# 圆形mask
x, y = np.ogrid[:800, :800]
mask = (x-400)**2 + (y-400)**2 > 380**2
mask = (255 * mask).astype('uint8')

wc = wc_module.WordCloud(
    font_path='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',
    width=800, height=800,
    background_color='white',
    max_words=60,
    mask=mask,
    color_func=green_color_func,
    prefer_horizontal=0.9,
    min_font_size=12,
    max_font_size=130,
).generate_from_frequencies(freq)

wc.to_file('/tmp/wc_green.png')
print("绿色词云生成完毕")

# 上传到飞书
ops = FeishuDocOperations(HOST, FEISHU_APPID, "https://id.lixiang.com/api",
    obtainIdaasClientId(), obtainIdaasClientSecret(), SERVICE_ID, USER_NAME, scopes=SCOPES)
token = ops._get_access_token()
fh = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

with open('/tmp/wc_green.png', 'rb') as f:
    img = f.read()

r1 = requests.post(
    f"{HOST}/proxy/open-apis/drive/v1/medias/upload_all?userName={USER_NAME}",
    files={'file': ('wc.png', img, 'image/png')},
    data={'file_name':'wc.png','parent_type':'docx_image','parent_node':IMAGE_BLOCK_ID,'size':str(len(img))},
    headers={"Authorization":f"Bearer {token}"}
).json()
print(f"上传: code={r1.get('code')}")

if r1.get('code') == 0:
    ft = r1['data']['file_token']
    r2 = requests.patch(
        f"{HOST}/proxy/open-apis/docx/v1/documents/{DOC_ID}/blocks/{IMAGE_BLOCK_ID}?userName={USER_NAME}",
        json={"replace_image":{"token":ft}}, headers=fh).json()
    print(f"替换: code={r2.get('code')}")
