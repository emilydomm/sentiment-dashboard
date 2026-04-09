#!/usr/bin/env python3
"""
每周舆情数据更新脚本
由 OpenClaw cron 调用，通过 Agent 执行 web_search 搜集过去7天的理想超充舆情数据
实际由 cron 任务调用 Agent message 触发，此脚本仅作参考说明
"""
# 此脚本的逻辑由 OpenClaw Agent (main session) 执行
# cron 任务直接发 message 给 Agent，Agent 负责：
# 1. web_search 搜集 T-7 超充舆情
# 2. 情感分析分类（正向/负向/中性）
# 3. 生成 YYYY-MM-DD.json 写入 docs/data/
# 4. 更新 dates.json
# 5. git push 到 GitHub
# 6. 等待 GitHub Pages 同步后用浏览器验证看板
# 7. 检查正负向分类是否合理，抽查3-5条
# 8. 与行业资讯一起通过飞书推送给馨姐
