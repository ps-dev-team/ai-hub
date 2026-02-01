# Coding Workflow

How AI agents should handle coding tasks. The orchestrator (Berto/Clawdbot) delegates to Claude Code for implementation.

## The Rule

**For all coding tasks, use Claude Code as the executor.** The orchestrator's job is to plan, delegate, monitor, and QA — not to hand-edit files directly.

```
Orchestrator (Berto)          Claude Code
├── Understands context   →   ├── Implements code
├── Plans the approach    →   ├── Runs tests
├── Creates tickets       →   ├── Fixes linting
├── Writes CLAUDE.md      →   ├── Commits changes
├── Dispatches tasks      →   └── Pushes branches
├── Monitors progress
├── Reviews output
└── Opens/manages PRs
```

## Why

- Claude Code has full project context (reads all files, understands dependencies)
- It's optimized for coding (tool use, file editing, terminal commands)
- The orchestrator stays free to monitor, plan, and handle multiple tasks
- Consistent quality — Claude Code follows CLAUDE.md rules every time
- Parallel work — multiple Claude Code instances on different tasks/branches

## Project Setup (One-Time)

Every project must have a `CLAUDE.md` at the root. This is Claude Code's instruction manual.

### CLAUDE.md Template

```markdown
# [project-name]

[One-line description of the project]

## Architecture

[Directory structure with brief descriptions]

## Commands

[All dev commands: install, dev, build, test, lint, format]

## Code Conventions

[Language, TypeScript config, formatting rules, naming conventions]

## Key Dependencies

[Important packages and what they're for]
```

### Optional: `.claude/rules/`

For path-scoped rules (e.g., different conventions for `src/blocks/` vs `src/lib/`):

```
.claude/
  rules/
    blocks.md        # Rules for src/blocks/**
    components.md    # Rules for src/components/**
    code-style.md    # Global code style rules
  skills/
    create-thing/    # Reusable task templates
```

Each rule file can have a frontmatter `paths` filter:

```yaml
---
paths:
  - "src/blocks/**/*.{ts,tsx}"
---
```

## Dispatching Tasks

### One-Shot Tasks (quick, focused)

```bash
exec pty:true workdir:~/project command:"claude 'Your task description here'"
```

### Background Tasks (longer work)

```bash
exec pty:true workdir:~/project background:true command:"claude 'Your task description here.

When completely finished, run: clawdbot gateway wake --text \"Done: [brief summary]\" --mode now'"
```

The wake command notifies the orchestrator immediately when Claude Code finishes.

### Task Prompt Best Practices

- **Be specific** — "Add error handling to the API calls in src/lib/gateway.ts" not "improve the code"
- **Reference files** — Tell Claude Code which files to look at
- **State the goal** — What should work when done? What test should pass?
- **Include constraints** — "Don't change the public API" or "Keep it under 100 lines"
- **Branch instructions** — "Work on branch feat/my-feature, commit when done"

### Example Prompt

```
Create the GlassCard component for the dashboard redesign.

Requirements:
- Create src/components/ui/glass-card.tsx
- Glassmorphism style: backdrop-blur-[20px], semi-transparent bg, subtle border
- Support light/dark variants via a theme prop
- Use Framer Motion for hover lift animation
- Export from src/components/ui/index.ts

Reference the Figma tokens in docs/figma/figma-tokens.json for exact values.

Work on branch feat/design-system-rebuild.
Run lint and typecheck before committing.
Commit with message "feat: add GlassCard component with glassmorphism styling"
```

## Monitoring

```bash
# Check if still running
process action:poll sessionId:XXX

# Read output
process action:log sessionId:XXX

# Send input if Claude Code asks a question
process action:submit sessionId:XXX data:"yes"

# Kill if stuck
process action:kill sessionId:XXX
```

## Quality Control (Orchestrator's Job)

After Claude Code finishes:

1. **Review the diff** — `git diff main..feat/branch`
2. **Run tests** — Make sure nothing broke
3. **Check lint/format** — CI should be green
4. **Open the PR** — With proper description, ticket links
5. **Update Notion** — Move ticket to In Review, add PR link

## Parallel Work

For multiple tasks, use git worktrees:

```bash
# Create worktrees
git worktree add -b feat/task-a /tmp/task-a main
git worktree add -b feat/task-b /tmp/task-b main

# Launch Claude Code in each
exec pty:true workdir:/tmp/task-a background:true command:"claude 'Task A...'"
exec pty:true workdir:/tmp/task-b background:true command:"claude 'Task B...'"

# Monitor both
process action:list

# Cleanup after
git worktree remove /tmp/task-a
```

## What the Orchestrator Should NOT Do

- ❌ Hand-edit source code files directly (use Claude Code)
- ❌ Write implementation code in chat responses
- ❌ Skip CLAUDE.md setup — it's mandatory for every project
- ❌ Fire-and-forget — always monitor and review Claude Code's output

## What the Orchestrator SHOULD Do

- ✅ Plan and break down tasks into clear prompts
- ✅ Set up CLAUDE.md and rules for each project
- ✅ Create and manage Notion tickets
- ✅ Dispatch tasks to Claude Code with specific instructions
- ✅ Monitor progress and handle blockers
- ✅ Review diffs and ensure quality
- ✅ Open PRs with proper descriptions
- ✅ Manage git workflow (branches, merges, rebases)
- ✅ Communicate progress to the human
