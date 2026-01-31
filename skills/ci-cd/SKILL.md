---
name: ci-cd
description: Set up and maintain CI/CD pipelines with GitHub Actions. Use when creating a new project pipeline, adding test/lint/build/deploy steps, or troubleshooting CI failures. Includes workflow templates for common stacks.
---

# CI/CD — GitHub Actions

Set up and maintain continuous integration and deployment pipelines.

## Philosophy

- Every PR must pass CI before review
- Pipeline should be fast (< 5 min for lint + test + build)
- Fail early: lint → types → tests → build → deploy
- Keep workflows DRY with reusable steps

## Standard Pipeline

Every project should have at minimum:

```
PR opened/updated → Lint → Type Check → Test → Build
Merge to main     → Build → Deploy
```

## Workflow Structure

Workflows live in `.github/workflows/` in the project repo.

### ci.yml — Runs on every PR

Steps (in order):
1. **Checkout** code
2. **Setup** runtime (Node, Bun, Python, etc.)
3. **Install** dependencies (with cache)
4. **Lint** — catch style/format issues
5. **Type check** — catch type errors
6. **Test** — run test suite
7. **Build** — verify it compiles

### deploy.yml — Runs on merge to main

Steps:
1. Everything from ci.yml
2. **Deploy** to hosting (Vercel, AWS, etc.)

## Templates

See `assets/` for ready-to-use workflow files:
- `ci-node.yml` — Node.js / Bun projects
- `deploy-vercel.yml` — Vercel deploy via GitHub Actions

## Best Practices

### Caching

Always cache dependencies to speed up runs:
```yaml
- uses: actions/cache@v4
  with:
    path: node_modules
    key: ${{ runner.os }}-node-${{ hashFiles('**/package-lock.json', '**/bun.lock') }}
```

### Secrets

- Never hardcode secrets in workflows
- Use GitHub repository secrets: `${{ secrets.SECRET_NAME }}`
- Document required secrets in the project README

### Notifications

- GitHub auto-comments on PR check failures
- For deploy failures: consider Slack notification step

### Branch Protection

Configure on GitHub:
- Require status checks to pass before merge
- Require PR reviews
- No direct pushes to main

## Troubleshooting

When CI fails:
1. Read the error in the GitHub Actions log
2. Reproduce locally: run the same commands from the workflow
3. Fix and push — CI re-runs automatically

```bash
# View failed logs
gh run view <run-id> --repo owner/repo --log-failed
```

Common issues:
- **Dependency mismatch** — delete lock file, reinstall, commit
- **Environment variable missing** — check secrets are set in repo settings
- **Flaky tests** — identify and fix or quarantine
- **Build cache stale** — clear cache and re-run
