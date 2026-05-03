import json, os
items = [
  {
    "title": "理想汽车公布2026年4月交付数据",
    "url": "https://www.lixiang.com/news/155.html",
    "publish_date": "2026-05-01",
    "keyword": "新车发布",
    "desc": "理想汽车4月交付34085辆，并披露全新理想L9 Livis已在北京车展全球首秀，搭载800V主动悬架、5C增程系统、全线控底盘和双马赫100芯片，5月15日将完整发布。",
    "image": ""
  },
  {
    "title": "小鹏GX全系车色亮相北京车展，小鹏第二代VLA智驾报告迎来首发",
    "url": "https://www.xiaopeng.com/news",
    "publish_date": "2026-04-30",
    "keyword": "智能驾驶",
    "desc": "小鹏官网资讯显示，小鹏GX在北京车展亮相，并发布第二代VLA相关内容；同页还披露新科技旗舰小鹏GX已于4月15日开启预售。",
    "image": ""
  },
  {
    "title": "五一车市观察：家庭出行需求增长，补能、智驾成消费新宠",
    "url": "https://c.m.163.com/news/a/KRUDPD4L05199LJK.html",
    "publish_date": "2026-05-01",
    "keyword": "智能驾驶",
    "desc": "中国商报五一假期走访显示，家庭用户购车更关注补能效率、换电和智能驾驶辅助，L2级辅助驾驶正加速成为主流车型标配。",
    "image": ""
  },
  {
    "title": "2026北京车展凸显汽车技术体系化竞争趋势",
    "url": "https://www.donews.com/news/detail/4/6529200.html",
    "publish_date": "2026-04-29",
    "keyword": "底盘技术",
    "desc": "DoNews聚焦北京车展技术路线变化，指出竞争重心正从单项参数转向安全、效率、补能和智能化的系统能力，线控底盘、800V高压平台与多传感器智驾成为看点。",
    "image": ""
  },
  {
    "title": "2026北京车展：科技引领美好生活，吉利汽车携全系产品技术亮相",
    "url": "https://www.cqn.com.cn/auto/content/2026-04/24/content_9154199.htm",
    "publish_date": "2026-04-24",
    "keyword": "底盘技术",
    "desc": "吉利在北京车展展示原生新能源越野架构和i-HEV智擎混动技术，强调AI扭矩分配、全地形模式、主动姿态调节以及高功率三电系统的整合能力。",
    "image": ""
  },
  {
    "title": "新科技旗舰小鹏GX正式开启预售，预售价39.98万元",
    "url": "https://www.xiaopeng.com/news",
    "publish_date": "2026-04-15",
    "keyword": "新车发布",
    "desc": "小鹏官网资讯页显示，小鹏GX已于4月15日开启预售，成为小鹏面向高端市场的新科技旗舰车型。",
    "image": ""
  }
]
path = '/workspace/sentiment-dashboard/docs/data/industry/2026-05-03.json'
os.makedirs(os.path.dirname(path), exist_ok=True)
text = json.dumps(items, ensure_ascii=False, indent=2)
json.loads(text)
with open(path, 'w', encoding='utf-8') as f:
    f.write(text)
print(path)
print('count=', len(items))
