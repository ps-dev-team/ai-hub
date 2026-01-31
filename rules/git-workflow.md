# Git Workflow

Rules for how all projects use Git and GitHub.

## Branching

- Branch from `main`, always
- One branch per task/feature
- Delete branch after merge
- Never commit directly to `main` — always use a PR

## Commits

- **1 PR = 1 commit** — squash locally before pushing if you iterated
- Follow Conventional Commits: `type: description`
- Imperative mood: "add" not "added"
- Subject under 72 characters, no trailing period

## Pull Requests

- **Atomic** — one concern per PR, small and focused
- **Description** — what changed, why, bullet list of specifics
- **Design links** — include Figma/design link when applicable
- **Screenshots** — mandatory for UI changes
- **PR link in ticket** — always add the PR URL to the Notion task Notes

## Merge Strategy

- **Rebase and merge** — keeps linear history
- Never merge commits, never fast-forward with merge bubbles
- Author squashes locally before push if multiple commits exist

## After Merge

```bash
git checkout main
git pull origin main
git branch -d feat/my-feature
```

## Code Review

- Fix CI before requesting review
- Address all review comments before re-requesting
- Resolve threads after fixing — don't leave them hanging
