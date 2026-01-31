---
name: notion
description: Notion-based project and task management. Use when creating, updating, or querying tasks, generating daily reports, tracking time, or managing project boards. Includes API reference for direct Notion API calls. Requires NOTION_API_KEY environment variable.
---

# Notion — Project & Task Management

Manage tasks, projects, and daily reports using Notion as the source of truth.

## Setup

Set the `NOTION_API_KEY` environment variable (starts with `ntn_` or `secret_`).

Create an integration at https://notion.so/my-integrations, then share target pages/databases with it.

## Database Structure

### Tasks Database

Columns:
| Property | Type | Description |
|---|---|---|
| Task | Title | Task name |
| Status | Select | Current state (see workflow below) |
| Priority | Select | `Urgent`, `High`, `Medium`, `Low` |
| Project | Select | Associated project |
| Due Date | Date | Deadline |
| Notes | Rich text | Additional context, links, decisions |
| Time Spent | Number | Minutes spent on implementation |
| Discussion Time | Number | Minutes spent in planning/discussion |
| Started At | Date | When work began |
| Completed At | Date | When marked as Done |

### Task Status Workflow

```
Backlog → Ready to Tackle → In Progress → In Review → Done
                                             ↘ Blocked
```

- **Backlog** — Captured, not yet prioritized
- **Ready to Tackle** — Prioritized, ready to start
- **In Progress** — Actively being worked on (set `Started At`)
- **In Review** — PR opened, awaiting review
- **Done** — Merged and complete (set `Completed At`)
- **Blocked** — Cannot proceed (add reason in Notes)

### Projects Database

Columns:
| Property | Type | Description |
|---|---|---|
| Project | Title | Project name |
| Status | Select | `Active`, `On Hold`, `Completed` |
| Repository | URL | GitHub repo link |
| Description | Rich text | What the project is about |

### Daily Dev Reports Database

Columns:
| Property | Type | Description |
|---|---|---|
| Report | Title | Report title (e.g., "2025-01-31 — Daily Report") |
| Date | Date | Report date |
| Tickets Completed | Number | Tasks moved to Done |
| Tickets In Progress | Number | Tasks currently in progress |
| Tickets Blocked | Number | Tasks currently blocked |
| PRs Opened | Number | Pull requests opened |
| PRs Merged | Number | Pull requests merged |
| Commits | Number | Commits pushed |
| Lines Changed | Number | Lines added + removed |
| Time Spent | Number | Total minutes spent |
| Token Cost | Number | AI token cost in $ |
| Projects | Multi-select | Projects worked on |
| Summary | Rich text | What was accomplished |

## Workflows

### Creating a Task

1. Create page in Tasks database with:
   - Title, Priority, Project
   - Status: `Backlog` (default) or `Ready to Tackle` if prioritized
2. Add context in Notes (requirements, links, decisions)

### Starting Work on a Task

1. Move status to `In Progress`
2. Set `Started At` to current timestamp
3. Create a feature branch following GitHub skill conventions

### Completing a Task

1. Open PR → move status to `In Review`
2. After merge → move status to `Done`
3. Set `Completed At` to current timestamp
4. Update `Time Spent` with total minutes

### Reviewing the Board

Query tasks by status to assess workload:

```bash
# Get all in-progress tasks
# POST /v1/databases/{db_id}/query with filter: Status = "In Progress"
```

See `references/api.md` for full API details.

### Generating a Daily Report

At end of day, create a report entry with:
1. Count tickets by status change (completed, in progress, blocked)
2. Count PRs opened/merged (from GitHub)
3. Count commits and lines changed (from git log)
4. Sum time spent across tasks
5. List projects worked on
6. Write a brief summary of accomplishments

### Time Tracking

Track time on each task:
- **Time Spent** — Implementation time (coding, testing, debugging)
- **Discussion Time** — Planning, review, meetings about the task
- Update after each work session, not just at completion

## API Reference

For Notion API endpoints, authentication, property formats, and query syntax, see `references/api.md`.
