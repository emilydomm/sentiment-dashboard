# 看板升级方案

## 改版需求

### 1. 总体架构
- **旧标题**: 理想超充舆情监测
- **新标题**: 智能电动传播资讯
- **栏目结构**: 
  - 栏目1: 理想超充舆情监测（保留现有功能）
  - 栏目2: 智能电动行业资讯（新增）

### 2. 数据源变更
- **舆情监测**: 只保留小红书数据，移除微博/抖音/资讯标签
- **行业资讯**: 每天全网搜索（web_search），8个关键词
  - 底盘、电池、电机、增程、充电、三电、能耗、悬架

### 3. 前端改动
- 双栏目 Tab 切换布局
- 舆情监测保持三栏（正向/负向/中性）
- 行业资讯采用时间线列表布局

## 已完成

✅ 2026-03-10 行业资讯数据抓取（7条）
  - 数据路径: `docs/data/industry/2026-03-10.json`
  - 数据来源: web_search 真实搜索结果
  - 包含关键词: 底盘(2条)、增程(1条)、三电(1条)、能耗(1条)、悬架(2条)

## 待完成

### 高优先级
1. [ ] 修改 `docs/index.html` 前端页面
   - 标题改为"智能电动传播资讯"
   - 添加 Tab 切换（舆情监测 / 行业资讯）
   - 移除舆情监测的微博/抖音/资讯筛选按钮
   - 行业资讯布局设计

2. [ ] 创建行业资讯自动化脚本
   - 脚本路径: `fetch_industry_news_auto.py`
   - 功能: 每天自动调用 web_search 搜索8个关键词
   - 输出: `docs/data/industry/YYYY-MM-DD.json`

3. [ ] 更新定时任务
   - 现有: 每天08:00 爬取小红书 + 生成舆情数据
   - 新增: 每天08:30 抓取行业资讯

### 中优先级
4. [ ] 优化行业资讯数据处理
   - 去重（相同URL）
   - 智能情感判断优化
   - 摘要长度控制

5. [ ] 前端UI优化
   - 行业资讯卡片样式
   - 关键词标签显示
   - 响应式适配

### 低优先级
6. [ ] 数据统计增强
   - 行业资讯按关键词统计
   - 趋势图表展示

## 技术方案

### 行业资讯抓取流程
```python
# 伪代码
keywords = ['底盘', '电池', '电机', '增程', '充电', '三电', '能耗', '悬架']
results = []

for keyword in keywords:
    search_results = web_search(
        query=f"{keyword} 新能源汽车",
        count=3
    )
    results.extend(parse_results(keyword, search_results))

save_to_file(f"industry/{today}.json", results)
```

### 前端架构
```html
<div class="tab-container">
  <div class="tabs">
    <button onclick="switchTab('sentiment')">理想超充舆情监测</button>
    <button onclick="switchTab('industry')">智能电动行业资讯</button>
  </div>
  
  <div id="sentiment-panel" class="active">
    <!-- 现有舆情监测内容 -->
  </div>
  
  <div id="industry-panel" style="display:none">
    <!-- 行业资讯列表 -->
  </div>
</div>
```

## 数据示例

### 行业资讯数据结构
```json
{
  "platform": "web",
  "note_id": "https://...",
  "title": "新能源汽车底盘，开始碾轧燃油车",
  "desc": "摘要内容...",
  "author": "行业资讯",
  "ip_location": "",
  "liked_count": 0,
  "comment_count": 0,
  "share_count": 0,
  "publish_date": "2026-03-10",
  "url": "https://...",
  "sentiment": "positive",
  "keyword": "底盘"
}
```

## 后续计划

1. **本周内**: 完成前端改版和行业资讯自动化脚本
2. **下周**: 观察数据质量，调优搜索策略
3. **长期**: 考虑增加更多垂直媒体数据源
