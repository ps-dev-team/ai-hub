# Slack Communication

Rules for how AI agents communicate on Slack.

## Two Communication Channels

### 1. Direct Messages (DM) — Conversation

Use the DM window for direct conversation with the human:
- Respond in the **main message window** (not as thread replies)
- Keep it conversational — this is where decisions happen
- When starting a task, confirm briefly here: _"On it, I'll post progress in #channel"_

### 2. Dedicated Log Channel — Work Reports

Use a dedicated channel for task execution, progress, and reports:
- Post a **single summary message** when starting a task (e.g., "Starting: implement TitleBlock component")
- All details, progress updates, and results go in a **thread** under that message
- This keeps the channel clean — one message per task, details in threads

### Pattern: Task Execution

```
#log-channel
├── 📌 "Starting: implement TitleBlock component"     ← main message
│   ├── "Reading Figma design tokens..."               ← thread
│   ├── "Created component with schema..."             ← thread
│   ├── "PR #15 opened: feat/add-title-block"          ← thread
│   └── "✅ Done — PR ready for review"                ← thread
├── 📌 "Daily Report — 2025-01-31"                     ← main message
│   ├── "Tickets: 3 completed, 2 in progress..."       ← thread
│   └── "Summary: focused on video editor blocks..."   ← thread
```

## Message Format

- Be concise — no filler words
- Use emoji for status: ✅ done, 🔄 in progress, ❌ failed, ⏳ waiting
- Code snippets in code blocks
- Link to PRs, issues, and relevant resources

## Threading Rules

| Context | Where | Threading |
|---|---|---|
| Conversation with human | DM | Main window (no threads) |
| Task started notification | DM | Brief message, no thread |
| Task execution details | Log channel | Thread under task message |
| Daily reports | Log channel | Summary as main message, details in thread |
| Alerts / urgent items | DM | Main window |

## Configuration

Each agent should define in its own config:
- **DM channel** — The direct message channel with the human
- **Log channel** — The dedicated channel for work reports and progress
