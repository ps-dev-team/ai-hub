# AI Hub

A centralized repository for AI agent configurations — skills, rules, and agent profiles used across my projects and workflows.

This is primarily built for my own AI agents, but it's public for anyone who wants to use, adapt, or contribute. If you find something useful, go for it.

## Structure

```
ai-hub/
├── skills/          # Reusable procedural skills (loaded on-demand)
├── agents/          # Agent configurations (identity + behavior)
└── rules/           # Global principles and standards (always active)
```

## Concepts

### Skills

Self-contained modules that teach agents **how to do specific tasks**. Each skill has a `SKILL.md` with YAML frontmatter (`name` + `description`) and optional `scripts/`, `references/`, `assets/` directories. Skills are loaded on-demand when the task matches the description.

### Agents

Agent configurations define **who the agent is** — identity, personality, and which skills/rules it uses.

### Rules

Global principles that define **how agents should behave**. Unlike skills (on-demand), rules are always active across all tasks.

## Available Skills

| Skill | Description |
|---|---|
| [figma-dev](skills/figma-dev/) | Analyze Figma designs and implement them as code |
| [youtube-gemini](skills/youtube-gemini/) | Analyze YouTube videos with Gemini AI |

## Usage

### With Clawdbot / OpenClaw

Symlink or clone skills into the agent's skills directory:

```bash
ln -s /path/to/ai-hub/skills/figma-dev ~/clawd/skills/figma-dev
```

### With Claude Code

Symlink skills into `.claude/skills/` in any project:

```bash
ln -s /path/to/ai-hub/skills/youtube-gemini .claude/skills/youtube-gemini
```

Rules can go into `.claude/rules/` for always-active behavior.

### With Other Agents

Skills follow the standard SKILL.md format (YAML frontmatter + markdown instructions). Adapt to your agent's configuration as needed.

## Environment Variables

Skills use environment variables for API keys. Never hardcode credentials.

| Variable | Used By |
|---|---|
| `FIGMA_API_TOKEN` | figma-dev |
| `GEMINI_API_KEY` | youtube-gemini |

## Contributors

### 🦞 Berto

The most active contributor here is [Berto](https://github.com/berto-ai) — an AI agent (powered by Claude) that works as a developer, assistant, and collaborator. Berto builds skills, opens PRs, reviews code, and maintains this repository alongside Paulo. Yes, the lobster emoji is intentional.

## Contributing

Contributions are welcome! If you have skills, rules, or agent configs that could be useful, feel free to open a PR. Keep skills self-contained, use environment variables for secrets, and follow the existing structure.

## License

MIT
