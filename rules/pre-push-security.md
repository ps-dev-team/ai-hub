# Pre-Push Security Check

## MANDATORY — Before Every Push/PR

Before pushing any branch or creating a PR, scan ALL staged/changed files for exposed secrets:

### Patterns to check

```
ntn_[A-Za-z0-9]+          # Notion tokens
sk-[A-Za-z0-9_-]+         # OpenAI keys
ghp_[A-Za-z0-9]+          # GitHub PATs
ghu_[A-Za-z0-9]+          # GitHub user tokens
ghs_[A-Za-z0-9]+          # GitHub server tokens
secret_[A-Za-z0-9]+       # Generic secrets
xoxb-[A-Za-z0-9-]+        # Slack bot tokens
xapp-[A-Za-z0-9-]+        # Slack app tokens
AIza[A-Za-z0-9_-]+        # Google API keys
AKIA[A-Za-z0-9]+          # AWS access keys
-----BEGIN.*PRIVATE KEY    # Private keys
```

### How to check

```bash
# Run this before every push:
git diff --cached --diff-filter=ACMR | grep -E 'ntn_|sk-|ghp_|ghu_|ghs_|secret_|xoxb-|xapp-|AIza|AKIA|PRIVATE KEY|password|api_key|apikey' -i
```

If ANY match is found → **STOP. Do not push.** Remove the secret, use environment variables instead.

### Rules

1. **NEVER hardcode secrets** in source files — use `process.env.VAR` or `$ENV_VAR`
2. **NEVER commit scripts with embedded tokens** — one-shot scripts stay local, never in the repo
3. **NEVER commit .env files** with real values — only `.env.example` with placeholder values
4. **If a secret is accidentally pushed** → rotate it immediately, even if force-pushed away (git history caches exist)
