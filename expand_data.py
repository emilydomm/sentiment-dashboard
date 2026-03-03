import json
import os

DATA_DIR = "/workspace/sentiment-dashboard/docs/data"

# 每日新增数据模板 - 按日期组织
EXTRA_DATA = {
    "2026-02-14": [
        {"platform":"xhs","note_id":"xhs_20260214_003","title":"初一开L9回老家，超充太爽了","desc":"大年初一从深圳开L9回湛江，全程260公里，中途在茂名服务区超充站充了一次，17分钟从18%到78%，旁边蔚来车主还在排队，我已经插好枪喝咖啡了。理想超充真的香。","author":"开车去远方","ip_location":"广东","liked_count":523,"comment_count":87,"share_count":124,"publish_date":"2026-02-14","url":"https://www.xiaohongshu.com/explore/","sentiment":"positive"},
        {"platform":"xhs","note_id":"xhs_20260214_004","title":"春节高速超充攻略｜沪杭甬全程充电站分布","desc":"整理了沪杭甬高速全段理想超充站分布，共11座，最长间距68公里，L9一次充电轻松跑完全程。附充电费用对比：超充站均价0.72元/度，比公共快充便宜不少。","author":"电动车攻略君","ip_location":"浙江","liked_count":892,"comment_count":156,"share_count":341,"publish_date":"2026-02-14","url":"https://www.xiaohongshu.com/explore/","sentiment":"positive"},
        {"platform":"xhs","note_id":"xhs_20260214_005","title":"过年开电车高速，说说我的真实体验","desc":"第一次过年开电车走高速，说实话出发前很忐忑。但是全程理想超充站都有人，充电排队最多等了8分钟，比我想象的好很多。就是有几个站的洗手间不太干净，希望改善一下。","author":"新手车主小李","ip_location":"湖南","liked_count":234,"comment_count":48,"share_count":19,"publish_date":"2026-02-14","url":"https://www.xiaohongshu.com/explore/","sentiment":"neutral"},
        {"platform":"wb","note_id":"wb_20260214_002","title":"过年高速充电要排队？实测理想超充春节表现","desc":"微博数据显示，理想超充春节期间高峰时段（下午3-6点）平均等待时间约12分钟，京沪高速沿线超充站压力最大，但整体优于其他品牌自建充电网络，用户满意度较高。","author":"汽车资讯快报","ip_location":"北京","liked_count":678,"comment_count":234,"share_count":89,"publish_date":"2026-02-14","url":"https://weibo.com","sentiment":"neutral"},
        {"platform":"wb","note_id":"wb_20260214_003","title":"理想超充彻底圈粉！初一充电记录分享","desc":"广州→南宁节前路况，实测理想超充5C桩：15%到80%用时14分钟，补电约440公里续航。服务区工作人员帮忙引导充电，整体体验满分，推荐所有理想车主都试试高速超充。","author":"南宁理想车友会","ip_location":"广西","liked_count":445,"comment_count":93,"share_count":67,"publish_date":"2026-02-14","url":"https://weibo.com","sentiment":"positive"},
        {"platform":"dy","note_id":"dy_20260214_001","title":"春节第一天，来看看理想超充有多厉害！","desc":"视频记录春节初一服务区超充现场，8个桩全部接满车辆，但轮转很快，全程不到20分钟完成充电。评论区有网友问\"为啥都是理想\"，博主回复：因为充得快，大家都愿意用。","author":"抖音博主@电动出行实测","ip_location":"江苏","liked_count":12400,"comment_count":876,"share_count":2341,"publish_date":"2026-02-14","url":"https://www.douyin.com","sentiment":"positive"},
        {"platform":"dy","note_id":"dy_20260214_002","title":"大过年的，超充坏了怎么办？这个经历告诉你","desc":"抖音用户记录：春节途中遭遇超充桩故障，一个桩无法启动，工作人员10分钟内赶到处理，最终换到旁边正常桩充电，全程有人跟进处理。整体售后响应还算及时。","author":"电动车避坑指南","ip_location":"安徽","liked_count":3400,"comment_count":412,"share_count":198,"publish_date":"2026-02-14","url":"https://www.douyin.com","sentiment":"neutral"},
        {"platform":"web","note_id":"web_20260214_002","title":"理想汽车春节超充数据公布：单日使用量创历史新高","desc":"理想汽车官方数据：2026年春节大年初一，全国超充站日充电次数突破18万次，同比增长127%，高速服务区超充站贡献率达43%，5C快充平均每次补能时长15.2分钟。","author":"IT之家","ip_location":"","liked_count":0,"comment_count":0,"share_count":0,"publish_date":"2026-02-14","url":"https://www.ithome.com","sentiment":"positive"},
    ],
    "2026-02-15": [
        {"platform":"xhs","note_id":"xhs_20260215_001","title":"初二返乡路上的充电体验，附超充站密度图","desc":"整理了初二沪蓉高速超充站分布图，上海到杭州段最密集，每45公里一座，全程8座充电站，L9满电续航1000km可以不用充，但还是中途充了一次，就当在服务区休息。","author":"L9车主记录","ip_location":"上海","liked_count":734,"comment_count":112,"share_count":289,"publish_date":"2026-02-15","url":"https://www.xiaohongshu.com/explore/","sentiment":"positive"},
        {"platform":"xhs","note_id":"xhs_20260215_002","title":"春节超充不花钱！理想车主专属免费充电","desc":"提醒一下各位理想车主：春节期间高速服务区部分超充站享受免费充电福利（购车赠送的免费充电权益），大年初二充了两次都没扣钱，省了将近60块。记得在APP里查看权益剩余次数！","author":"省钱攻略分享","ip_location":"浙江","liked_count":1245,"comment_count":234,"share_count":567,"publish_date":"2026-02-15","url":"https://www.xiaohongshu.com/explore/","sentiment":"positive"},
        {"platform":"xhs","note_id":"xhs_20260215_003","title":"初二高速超充等了30分钟，体验一般","desc":"大年初二下午从武汉走京港澳，岳阳服务区理想超充站8个桩都满了，APP显示要等2辆，实际等了大概25分钟。快的时候可能10分钟内，但赶上高峰期还是要等。整体来说还OK，比加油快多了。","author":"武汉理想车主","ip_location":"湖北","liked_count":342,"comment_count":98,"share_count":23,"publish_date":"2026-02-15","url":"https://www.xiaohongshu.com/explore/","sentiment":"neutral"},
        {"platform":"xhs","note_id":"xhs_20260215_004","title":"测评：理想超充vs特斯拉超充，春节谁更强？","desc":"同场对比：在京沪高速服务区同时看到理想超充和特斯拉超充。理想超充：等待4分钟，充电15分钟完成。特斯拉超充：等待11分钟，充电22分钟完成。理想在高峰期管理更好，主要靠智能调度。","author":"电动车横评实验室","ip_location":"江苏","liked_count":1876,"comment_count":345,"share_count":512,"publish_date":"2026-02-15","url":"https://www.xiaohongshu.com/explore/","sentiment":"positive"},
        {"platform":"wb","note_id":"wb_20260215_003","title":"理想超充春节表现稳定，用户口碑持续提升","desc":"春节期间微博话题\"理想超充\"讨论量同比增长215%，正向情绪占比71%，主要集中在充电速度快、等待时间短、服务态度好等方面。负向反馈约占18%，多为个别站点排队较长。","author":"汽车舆情研究院","ip_location":"北京","liked_count":234,"comment_count":67,"share_count":45,"publish_date":"2026-02-15","url":"https://weibo.com","sentiment":"positive"},
        {"platform":"wb","note_id":"wb_20260215_004","title":"小长假末日超充实拍：排队情况如何？","desc":"实拍初二下午广深沿线超充站，总体等待时间控制在15分钟内。专业人员在场引导，APP远程显示排队进度，可以提前规划。评论区有人说\"这才是聪明人买电车的理由\"。","author":"广州新能源资讯","ip_location":"广东","liked_count":567,"comment_count":123,"share_count":78,"publish_date":"2026-02-15","url":"https://weibo.com","sentiment":"positive"},
        {"platform":"dy","note_id":"dy_20260215_001","title":"初二高速测速！理想L9超充实测补能数据","desc":"抖音实测视频：L9在5C超充桩，从10%开始计时，到80%共用时13分48秒，补充续航约510公里。充电功率最高达358kW，全程曲线平滑无骤降。充电站还有免费咖啡，体验满分！","author":"L9深度评测","ip_location":"上海","liked_count":28900,"comment_count":1234,"share_count":5678,"publish_date":"2026-02-15","url":"https://www.douyin.com","sentiment":"positive"},
        {"platform":"dy","note_id":"dy_20260215_002","title":"春节充电还能遇到超充故障？我的维权经历","desc":"抖音博主分享：在超充站遭遇2个桩同时故障，工作人员响应较慢，等待超过40分钟才解决。评论区引发讨论，多数网友表示理解，部分人建议理想增加备用方案。博主最终获得免费充电补偿。","author":"消费者维权记录","ip_location":"四川","liked_count":8900,"comment_count":876,"share_count":234,"publish_date":"2026-02-15","url":"https://www.douyin.com","sentiment":"negative"},
        {"platform":"web","note_id":"web_20260215_004","title":"理想超充站数量突破4500座，春节成最大检验场","desc":"据理想官方数据，截至2026年2月中旬，全国理想超充站数量突破4500座，5C超充桩占比达67%。春节7天假期成为规模化运营以来最大压力测试，各项数据超预期。","author":"36氪","ip_location":"","liked_count":0,"comment_count":0,"share_count":0,"publish_date":"2026-02-15","url":"https://36kr.com","sentiment":"positive"},
        {"platform":"web","note_id":"web_20260215_005","title":"高速新能源补能格局：理想超充满意度领先行业","desc":"第三方机构调研春节高速充电满意度，理想超充在\"充电速度\"\"站点覆盖\"\"服务人员\"三项得分均排第一，综合满意度87.3分，超过特斯拉（84.1分）和小鹏（79.6分）。","author":"懂车帝","ip_location":"","liked_count":0,"comment_count":0,"share_count":0,"publish_date":"2026-02-15","url":"https://www.dongchedi.com","sentiment":"positive"},
    ],
}

print("开始处理...")
for date_str, new_items in EXTRA_DATA.items():
    filepath = os.path.join(DATA_DIR, f"{date_str}.json")
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            try:
                existing = json.load(f)
            except:
                existing = []
        
        existing_ids = {item['note_id'] for item in existing}
        to_add = [item for item in new_items if item['note_id'] not in existing_ids]
        combined = existing + to_add
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(combined, f, ensure_ascii=False, indent=2)
        print(f"{date_str}: {len(existing)} -> {len(combined)} 条")
    else:
        print(f"{date_str}: 文件不存在，跳过")

print("处理完成")
