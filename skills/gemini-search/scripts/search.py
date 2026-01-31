#!/usr/bin/env python3
"""
Gemini Search - Web search using Google Gemini with Google Search grounding.

Usage:
    python search.py "your search query" [--count N] [--pretty]

Environment:
    GEMINI_API_KEY - Your Gemini API key

Output:
    JSON with search results including titles, URLs, and snippets.
"""

import argparse
import json
import os
import sys

from google import genai
from google.genai import types


def get_api_key() -> str:
    """Get Gemini API key from environment variable."""
    key = os.environ.get("GEMINI_API_KEY")
    if not key:
        print("Error: GEMINI_API_KEY environment variable not set.", file=sys.stderr)
        sys.exit(1)
    return key


def search(query: str, count: int = 5) -> dict:
    """Perform a web search using Gemini with Google Search grounding."""
    api_key = get_api_key()
    client = genai.Client(api_key=api_key)

    prompt = f"""Search the web for: {query}

Provide the top {count} most relevant results. For each result, include:
1. Title
2. URL
3. A brief snippet/description

Format your response as a JSON array with objects containing "title", "url", and "snippet" fields.
Only output the JSON array, nothing else."""

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                tools=[types.Tool(google_search=types.GoogleSearch())],
            )
        )

        text = response.text.strip()

        # Remove markdown code blocks if present
        if text.startswith("```"):
            lines = text.split("\n")
            if lines[-1].strip() == "```":
                text = "\n".join(lines[1:-1])
            else:
                text = "\n".join(lines[1:])

        try:
            results = json.loads(text)
            return {"ok": True, "results": results, "query": query}
        except json.JSONDecodeError:
            return {"ok": True, "raw": text, "query": query}

    except Exception as e:
        return {"error": str(e), "query": query}


def main():
    parser = argparse.ArgumentParser(description="Search the web using Gemini")
    parser.add_argument("query", help="Search query")
    parser.add_argument("--count", "-n", type=int, default=5, help="Number of results (default: 5)")
    parser.add_argument("--pretty", "-p", action="store_true", help="Pretty print JSON output")

    args = parser.parse_args()

    result = search(args.query, args.count)

    if args.pretty:
        print(json.dumps(result, indent=2))
    else:
        print(json.dumps(result))


if __name__ == "__main__":
    main()
