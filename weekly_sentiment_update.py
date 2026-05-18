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
# 8. 通过飞书仅推送给馨姐个人：user:ou_dfa6d78ac7f1e08b474d766109b9fea7
# 9. 严禁发送到任何群组；若历史配置/默认目标含群组，必须覆盖移除后再发送
# 10. 双保险：执行前必须确认唯一发送目标仍是馨姐个人，且任务提示/配置里不存在任何群目标或“同时发群”要求
# 11. 若运行结果出现任何 group/chat 发送记录，视为失败，必须先修复再结束
