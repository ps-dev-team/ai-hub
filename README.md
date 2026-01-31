# AI Hub

Centralized AI configuration for agents, skills, and rules.

## Structure

```
ai-hub/
├── skills/          # Reusable procedural skills (on-demand)
├── agents/          # Agent configurations (identity + behavior)
└── rules/           # Global principles and standards (always active)
```

## Concepts

### Skills

Self-contained modules that teach agents **how to do specific tasks**. Loaded on-demand when the task matches the skill description. Each skill has a `SKILL.md` with YAML frontmatter and optional `scripts/`, `references/`, `assets/` directories.

### Agents

Agent configurations define **who the agent is** — identity, personality, and which skills/rules apply. Each agent directory contains the files needed to configure a specific AI agent.

### Rules

Global principles that define **how agents should behave**. Unlike skills (loaded on-demand), rules are always active and apply across all tasks.

## Usage

### With Clawdbot

Clone or symlink skills into the agent's skills directory:

```bash
ln -s /path/to/ai-hub/skills/figma-dev ~/clawd/skills/figma-dev
```

### With Claude Code

Copy or symlink skills into `.claude/skills/` in any project:

```bash
ln -s /path/to/ai-hub/skills/figma-dev .claude/skills/figma-dev
```

Rules can go into `.claude/rules/` for always-active behavior.

### With Other Agents

Skills follow the standard SKILL.md format (YAML frontmatter + markdown body). Adapt to your agent's configuration format as needed.

## Environment Variables

Skills use environment variables for API keys and secrets. Never hardcode credentials.

| Variable | Used By |
|---|---|
| `FIGMA_API_TOKEN` | figma-dev |
| `GEMINI_API_KEY` | youtube-gemini, gemini-search |
