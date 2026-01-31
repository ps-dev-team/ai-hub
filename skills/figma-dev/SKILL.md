---
name: figma-dev
description: Analyze Figma designs and implement them as code. Use when the user shares a Figma link or asks to implement a design from Figma. Supports visual analysis of artboards, extracting design tokens (colors, fonts, spacing), identifying components, and generating React/CSS code. Requires FIGMA_API_TOKEN environment variable.
---

# Figma Dev

Analyze Figma files like a developer: understand context visually, then extract precise values via API.

## Setup

Set the `FIGMA_API_TOKEN` environment variable with a Figma Personal Access Token.

Generate at: https://www.figma.com/developers → Personal Access Tokens

## Workflow

### 1. Visual Analysis (understand context)

Export artboards as images and analyze the design holistically:
- Layout structure, grid system, visual hierarchy
- Recurring patterns, component candidates
- Responsive breakpoints, interaction hints
- Design language and overall feel

```bash
uv run {baseDir}/scripts/figma_export.py --file-key <KEY> --format png --scale 2
```

Use the `image` tool to analyze exported artboards visually.

### 2. API Deep Dive (extract precise values)

Query the Figma REST API for exact values:

```bash
# Extract design tokens (colors, fonts, spacing, effects)
uv run {baseDir}/scripts/figma_tokens.py --file-key <KEY>

# Inspect specific nodes
uv run {baseDir}/scripts/figma_inspect.py --file-key <KEY> --node-ids <IDS>
```

### 3. Component Mapping

From the analysis, identify:
- Reusable components → React components
- Design tokens → CSS variables / Tailwind config
- Layout patterns → CSS Grid/Flexbox structure
- Typography scale → font size/weight/line-height tokens
- Color palette → color tokens
- Spacing system → spacing scale

### 4. Implementation

Generate code based on extracted data. Match the project's existing stack and conventions.

### 5. Visual QA

Compare implementation against design by placing screenshots side by side.

## Parsing Figma URLs

Extract file key and node IDs from URLs:
- File: `https://www.figma.com/design/<FILE_KEY>/<name>`
- Node: `https://www.figma.com/design/<FILE_KEY>/<name>?node-id=<NODE_ID>`
- Node IDs in URLs use `-` as separator; convert to `:` for API calls (e.g., `1-2` → `1:2`)

## API Reference

Base URL: `https://api.figma.com`

Key endpoints — see `references/api.md` for full details:
- `GET /v1/files/:key` — full file JSON (use `depth` to limit)
- `GET /v1/files/:key/nodes?ids=` — specific nodes
- `GET /v1/images/:key?ids=&format=png&scale=2` — render nodes as images
- `GET /v1/files/:key/styles` — published styles

Auth header: `X-Figma-Token: <token>`
