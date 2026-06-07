# NOTES

## Messaging rules for industry-news automation

- Industry news updates must be sent **only to 馨姐's personal Feishu chat**.
- Personal target: `user:ou_dfa6d78ac7f1e08b474d766109b9fea7`
- **Never send industry news updates to any Feishu group**.
- Forbidden group target example: `chat:oc_1e7043c8d90c241ad6b4a1dabab8a0e8`
- If any existing script, cron job, legacy config, remembered target, or auto-generated send step conflicts with this rule, this rule overrides it.
- Treat this as a hard constraint, not a preference: if a run summary shows any group send for industry news, it is a bug and must be removed before the next run.
- Delivery format is also a hard constraint: industry news must be sent as a **Feishu card**, never plain text.
- Sender implementation hard-gate: `/workspace/sentiment-dashboard/send_industry_feishu_card.py`
  - must construct a non-empty `presentation.blocks`
  - must carry a non-empty `presentation.title`
  - must target only `user:ou_dfa6d78ac7f1e08b474d766109b9fea7`
  - must reject any text-send path or text flags (`--message`, `--text`, `--markdown`, `--md`)
  - if card payload validation fails, the job must stop instead of falling back to plain text
- Double-insurance check: before running or editing the industry-news automation, verify both of these are true:
  1. the only allowed delivery target is `user:ou_dfa6d78ac7f1e08b474d766109b9fea7`
  2. no prompt / config / summary text contains any group target, group chat_id, or instruction to send to a group
- If either check fails, treat the job as misconfigured and fix it before the run.
- Once 馨姐 has already given a clear instruction, execute it immediately; do not repeatedly ask for reconfirmation.

Recorded on 2026-05-17 after repeated user clarification.
Updated on 2026-05-18 after an erroneous group send recurrence.
