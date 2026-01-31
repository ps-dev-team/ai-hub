---
name: gemini-search
description: Web search using Google Gemini with grounding. Use when web_search is unavailable or returns a Brave API key error. Provides search results with titles, URLs, and snippets.
---

# Gemini Search

Web search alternative using Google Gemini's grounding feature with Google Search.

## Setup

Set the `GEMINI_API_KEY` environment variable.

## When to Use

- When `web_search` fails due to missing Brave API key
- When you need web search results and have a Gemini API key available

## Usage

```bash
export GEMINI_API_KEY="your-api-key"
python scripts/search.py "your query" --count 5 --pretty
```

## Arguments

- `query` — The search query (required)
- `--count N` / `-n N` — Number of results (default: 5)
- `--pretty` / `-p` — Pretty print JSON output

## Output

JSON object with:
- `ok: true` on success
- `results` — Array of `{title, url, snippet}` objects
- `query` — The original query
- `error` — Error message if failed

## Dependencies

Requires `google-genai` package:
```bash
pip install google-genai
```
