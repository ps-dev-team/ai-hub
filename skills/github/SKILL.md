---
name: github
description: GitHub workflow conventions and gh CLI usage. Use when working with PRs, branches, commits, issues, or code reviews on GitHub. Covers branch naming, commit format, PR workflow, code review, and CI troubleshooting.
---

# GitHub Workflow

Standard GitHub workflow for all projects. Uses `gh` CLI for all operations.

## Branch Naming

```
<type>/<short-description>
```

Types: `feat`, `fix`, `refactor`, `chore`, `docs`, `test`, `ci`

Examples:
- `feat/add-title-block`
- `fix/transcription-timing`
- `chore/update-dependencies`

Keep descriptions short, lowercase, hyphen-separated.

## Commit Messages

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>: <description>

[optional body with details]
```

Types: `feat`, `fix`, `refactor`, `chore`, `docs`, `test`, `ci`, `style`, `perf`

Examples:
```
feat: add TitleBlock component with animation support
fix: correct timing offset in transcription parser
chore: update Tailwind to v4.1
```

Rules:
- Imperative mood ("add" not "added")
- No period at the end of the subject line
- Body explains **what** and **why**, not how
- Keep subject under 72 characters

## PR Workflow

### Creating a PR

1. Create a feature branch from `main`
2. Make focused, atomic changes (1 PR = 1 concern)
3. Push and open PR via CLI:

```bash
git checkout -b feat/my-feature
# ... make changes ...
git add -A && git commit -m "feat: description"
git push origin feat/my-feature
gh pr create --title "feat: description" --body "## Changes\n\n- Detail 1\n- Detail 2"
```

### PR Description

Always include:
- **What** changed (brief summary)
- **Why** (context/motivation)
- Bullet list of specific changes
- **Design link** — If there's an associated design (Figma, etc.), include the link
- **Screenshots** — Required for UI changes. Capture the result and embed in the PR body

### Screenshots for UI Changes

When a PR includes visual/UI changes, screenshots are **mandatory**:

1. Run the app locally (dev server or build)
2. Capture screenshots of the affected views
3. Embed in the PR body using markdown:

```markdown
## Screenshots

![Description](url-to-image)
```

Upload images via `gh` CLI:
```bash
# GitHub accepts images pasted in PR body or uploaded via the web UI
# From CLI, use issue/PR body with image URLs or base64
```

For before/after comparisons, use a table:
```markdown
| Before | After |
|--------|-------|
| ![before](url) | ![after](url) |
```

### Merge Strategy

- **1 PR = 1 squashed commit** on merge
- Merge method: **squash and merge** (or rebase if single commit)
- Branch is deleted after merge

### After Merge

```bash
git checkout main
git pull origin main
git branch -d feat/my-feature
```

## Code Review

### As Author

- Self-review the diff before requesting review
- Keep PRs small and focused — easier to review
- Respond to all comments before re-requesting review

### As Reviewer

- Check: correctness, readability, consistency with project conventions
- Approve with ✅ or request changes with specific feedback
- Don't nitpick style if linters/formatters handle it

## CI / Checks

### Check PR status

```bash
gh pr checks <number> --repo owner/repo
```

### Debug failures

```bash
# List recent runs
gh run list --repo owner/repo --limit 5

# View run details
gh run view <run-id> --repo owner/repo

# View only failed logs
gh run view <run-id> --repo owner/repo --log-failed
```

### Common fixes

- **Lint failures** → Run the project's lint/format command locally, commit the fix
- **Type errors** → Check the error, fix types, push
- **Test failures** → Run tests locally first: `npm test` / `bun test`
- **Build failures** → Run build locally: `npm run build` / `bun run build`

Always fix CI before requesting review.

## Issues

### Create

```bash
gh issue create --title "Bug: description" --body "## Steps to reproduce\n\n1. ...\n2. ..."
```

### Reference in PRs

Link issues in PR body: `Closes #123` or `Fixes #123`

## Useful Commands

```bash
# List open PRs
gh pr list --repo owner/repo

# View PR diff
gh pr diff <number> --repo owner/repo

# Check out a PR locally
gh pr checkout <number>

# List issues
gh issue list --repo owner/repo --state open

# API queries with jq
gh api repos/owner/repo/pulls/<number> --jq '.title, .state'

# JSON output with filtering
gh pr list --json number,title --jq '.[] | "\(.number): \(.title)"'
```
