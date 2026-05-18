# NOTES

## Messaging rules for industry-news automation

- Industry news updates must be sent **only to 馨姐's personal Feishu chat**.
- Personal target: `user:ou_dfa6d78ac7f1e08b474d766109b9fea7`
- **Never send industry news updates to any Feishu group**.
- Forbidden group target example: `chat:oc_1e7043c8d90c241ad6b4a1dabab8a0e8`
- If any existing script, cron job, legacy config, remembered target, or auto-generated send step conflicts with this rule, this rule overrides it.
- Treat this as a hard constraint, not a preference: if a run summary shows any group send for industry news, it is a bug and must be removed before the next run.
- Once 馨姐 has already given a clear instruction, execute it immediately; do not repeatedly ask for reconfirmation.

Recorded on 2026-05-17 after repeated user clarification.
Updated on 2026-05-18 after an erroneous group send recurrence.
