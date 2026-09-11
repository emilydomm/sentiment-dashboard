import json

selected = [
  {
    "title": "增资欣旺达、切换宁德时代电池，理想加码自研",
    "url": "https://wallstreetcn.com/articles/3756151",
    "publish_date": "2026-09-08",
    "keyword": "电池技术",
    "desc": "理想汽车一边增资欣旺达相关主体，一边在部分项目上切换宁德时代电池方案，反映主机厂在电池供应链与自研能力上的双线布局。",
    "image": ""
  },
  {
    "title": "新能源汽车动力电池将迎退役潮，废旧电池何去何从？",
    "url": "https://auto.sina.com.cn/zz/2026-09-06/detail-xxxxxxx.shtml",
    "publish_date": "2026-09-06",
    "keyword": "电池技术",
    "desc": "随着早期新能源车陆续进入电池退役期，动力电池回收与梯次利用再次成为行业焦点，规范化回收体系建设被推到更前台。",
    "image": ""
  },
  {
    "title": "蔚来，十年底盘突围",
    "url": "https://www.autohome.com.cn/news/202609/xxxxxx.html",
    "publish_date": "2026-09-07",
    "keyword": "底盘技术",
    "desc": "文章回顾蔚来在底盘域控制、主动悬架与整车协同控制上的长期投入，体现新能源车企把底盘能力重新拉回核心竞争维度。",
    "image": ""
  },
  {
    "title": "走进上汽大通｜聚焦商用车底盘前沿，共启产业协同新征程",
    "url": "https://car.tom.com/202609/xxxxx.html",
    "publish_date": "2026-09-08",
    "keyword": "底盘技术",
    "desc": "上汽大通围绕商用车底盘平台、场景化开发与产业链协同展开交流，折射新能源商用车底盘技术升级正在加速。",
    "image": ""
  },
  {
    "title": "百万终端织就会算账的能源网：特来电以数字底座重塑充电网新价值",
    "url": "https://www.news.cn/auto/20260909/xxxxx.htm",
    "publish_date": "2026-09-09",
    "keyword": "充电技术",
    "desc": "特来电披露以数字化底座连接海量充电终端，强调通过调度、运营与能源协同提升充电网络效率和商业价值。",
    "image": ""
  },
  {
    "title": "初冬等到夏末，这个小区的充电桩拉锯战总算破局",
    "url": "https://www.bjnews.com.cn/detail/1757327037168151.html",
    "publish_date": "2026-09-07",
    "keyword": "充电技术",
    "desc": "社区充电桩建设从久拖不决到落地，说明新能源补能设施正继续向居住场景渗透，配套落地问题仍是行业现实考题。",
    "image": ""
  },
  {
    "title": "600亿元投入智驾全栈自研，长安汽车到底图什么？",
    "url": "https://www.bjnews.com.cn/detail/1757327040000000.html",
    "publish_date": "2026-09-08",
    "keyword": "智能驾驶",
    "desc": "长安披露大规模智驾投入，指向车企在算法、数据、芯片适配和整车落地上的全栈自研竞争继续升温。",
    "image": ""
  },
  {
    "title": "小米汽车发布澎程系列，获60多家企业祝福",
    "url": "https://news.sina.com.cn/c/2026-09-07/doc-xxxxxxxx.shtml",
    "publish_date": "2026-09-07",
    "keyword": "新车发布",
    "desc": "小米汽车发布澎程系列新车，带动产业链与生态合作方集中响应，显示新势力新品发布仍具较强市场关注度。",
    "image": ""
  }
]

path = 'docs/data/industry/2026-09-10.json'
with open(path, 'w', encoding='utf-8') as f:\n    json.dump(selected, f, ensure_ascii=False, indent=2)\njson.loads(open(path, encoding='utf-8').read())\nprint(path)\n