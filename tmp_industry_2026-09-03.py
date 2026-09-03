import json
from pathlib import Path

items = [
  {
    "title": "AI+动力电池,加出怎样的新未来?聚焦2026世界动力电池大会",
    "url": "https://news.google.com/rss/articles/CBMiTkFVX3lxTE5LTko4cFVvYzBidDZjUTlKcHRsUTNkZkViLUIxVFYzTVFpY3lTN1VVai1jQlduTWFVdWNNQ2dZSXdMNEVNN0MtWlRrdUY0Zw?oc=5",
    "publish_date": "2026-09-02",
    "keyword": "电池技术",
    "desc": "文章发表于9月2日,围绕2026世界动力电池大会讨论AI与动力电池融合方向,涉及研发、制造和产业协同等趋势。",
    "image": ""
  },
  {
    "title": "2026世界动力电池大会启幕前夜,这场对话透露了哪些信号?",
    "url": "https://news.google.com/rss/articles/CBMiZkFVX3lxTE04MEJFRHFHdEJxRUQyQ0VvMHhLWVdNeVFXVW40SV9qdkllejhGWXNXc2hwUWw0ZHJoTmdaaHR4NGF2Mm9Hc2dLUlM2SmduQ19zRzlvUkdqUjdVcnI4dGZxalgwVDFWUQ?oc=5",
    "publish_date": "2026-09-02",
    "keyword": "电池技术",
    "desc": "文章发表于9月2日,聚焦动力电池大会前夜的行业对话,释放出动力电池技术演进与产业链合作的新信号。",
    "image": ""
  },
  {
    "title": "领航十五五 中国一汽向新行",
    "url": "https://news.google.com/rss/articles/CBMiakFVX3lxTE5ZZzNydUU5ejhmSGxfZDhFRGU0am85X3pUeEFuTktVLXlpTG5rR054a0VscVhST0IwUkdidjZWRmFpMmZmTlVRV0RmVEF1N0YxQlhSNFZ0OXd1ZGpHWTV3aUR6dUNSRzYtRlE?oc=5",
    "publish_date": "2026-09-01",
    "keyword": "底盘技术",
    "desc": "人民网9月1日报道中国一汽推进新能源与智能化布局,内容涉及整车架构、关键零部件和核心技术升级方向。",
    "image": ""
  },
  {
    "title": "3400公里充换电干线加速成网,宁夏探索交通能源融合新路径",
    "url": "https://news.google.com/rss/articles/CBMiY0FVX3lxTE9nWU5pX0lNV1V2cjJfWjRvazdDTVA4ZmFiRm5sZE1DVmYxM3Q1V2k0X2VxU0RaVUh0aWw1eWNpQ3NrY3J4cDdYd0xvZ3BJQlVhLWh4WHp1SFJMQjVBOURVYlVjRUc0V3h5QQ?oc=5",
    "publish_date": "2026-09-01",
    "keyword": "充电技术",
    "desc": "文章发表于9月1日,报道宁夏建设3400公里充换电干线网络,展现新能源补能基础设施与交通能源融合的最新进展。",
    "image": ""
  },
  {
    "title": "涉新能源、智能驾驶等运行安全 市场监管总局修订发布强制性国家标准",
    "url": "https://news.google.com/rss/articles/CBMiaEFVX3lxTE5CM204cjI2c2NCbWgtRkExU195aWNCUmk2MEEyd0hJUThCS2F6M2wzOEVXV2VSTThoUGNWcUVjaDhTcGxxZlc2TUkxVnZVbFhPaVh2NGVlSHJJQXZDQjVnZ0ZtcVY1X1dw?oc=5",
    "publish_date": "2026-08-31",
    "keyword": "智能驾驶",
    "desc": "中国新闻网8月31日报道新版强制性国标发布,覆盖新能源与智能驾驶运行安全,对单踏板制动等关键要求作出规范。",
    "image": ""
  },
  {
    "title": "明年7月实施!机动车运行安全技术条件强制性国标发布",
    "url": "https://news.google.com/rss/articles/CBMiZkFVX3lxTE5mcjVOUWdlOXFEZGN4bXc4QkY0TkVwaDRBZC15czkxbExNb3ZJSDQyUThqSjdEQWhJbWhoMWRSQU1EZEcxZmwyc3RWODRHUEtUa3Q0a2hqSlVCellFSHo0Q2twNjRNUQ?oc=5",
    "publish_date": "2026-08-31",
    "keyword": "智能驾驶",
    "desc": "文章发表于8月31日,解读机动车运行安全技术条件强制性国标,新增对商用车主动安全和智能驾驶相关要求的规范。",
    "image": ""
  },
  {
    "title": "售价超50万元 新一代理想MEGA发布 年底海外上市",
    "url": "https://news.google.com/rss/articles/CBMiVkFVX3lxTE9hX2cxQ2JGc3pkMFBXb2VaTjNkd1YxY3A2NW1QeTdVa1M3UEdWcWZnUG45VW9TRzNCQ3dIR2xvdDFJUVQ2QmM4a0Z1WVNkY0VhWnNqQzRQ?oc=5",
    "publish_date": "2026-09-02",
    "keyword": "新车发布",
    "desc": "证券时报9月2日报道新一代理想MEGA正式发布,售价超过50万元,并披露该车型计划于年底推进海外上市。",
    "image": ""
  }
]

for item in items:
    for k, v in item.items():
        if isinstance(v, str) and any(ch in v for ch in "“”‘’"):
            raise ValueError(f"Chinese quotes found in {k}: {v}")

text = json.dumps(items, ensure_ascii=False, indent=2)
json.loads(text)
out = Path('/workspace/sentiment-dashboard/docs/data/industry/2026-09-03.json')
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(text + '\n', encoding='utf-8')
print(f"wrote {out}")
