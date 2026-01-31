#!/usr/bin/env python3
"""
YouTube Video Processor - Analyze YouTube videos using Gemini.

Usage:
    python process_video.py <youtube_url> "<prompt>"

Environment:
    GEMINI_API_KEY - Your Gemini API key

Examples:
    python process_video.py "https://youtube.com/watch?v=xyz" "Summarize this video"
    python process_video.py "https://youtu.be/xyz" "What are the main points from a developer's perspective?"
"""

import argparse
import json
import os
import re
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


def extract_video_id(url: str) -> str:
    """Extract YouTube video ID from various URL formats."""
    patterns = [
        r'(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([a-zA-Z0-9_-]{11})',
        r'youtube\.com\/shorts\/([a-zA-Z0-9_-]{11})',
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return url  # Assume it's already a video ID


def process_video(url: str, prompt: str) -> dict:
    """Process a YouTube video with Gemini using the given prompt."""
    api_key = get_api_key()
    video_id = extract_video_id(url)
    youtube_url = f"https://www.youtube.com/watch?v={video_id}"

    client = genai.Client(api_key=api_key)

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=[
                types.Part.from_uri(
                    file_uri=youtube_url,
                    mime_type="video/*"
                ),
                prompt
            ]
        )

        return {
            "ok": True,
            "video_url": youtube_url,
            "video_id": video_id,
            "prompt": prompt,
            "result": response.text
        }

    except Exception as e:
        return {
            "error": str(e),
            "video_url": youtube_url,
            "prompt": prompt
        }


def main():
    parser = argparse.ArgumentParser(description="Process YouTube videos with Gemini")
    parser.add_argument("url", help="YouTube video URL or ID")
    parser.add_argument("prompt", help="What to analyze/extract from the video")
    parser.add_argument("--json", "-j", action="store_true", help="Output raw JSON")

    args = parser.parse_args()

    result = process_video(args.url, args.prompt)

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        if result.get("ok"):
            print(f"Video: {result['video_url']}\n")
            print(f"Prompt: {result['prompt']}\n")
            print("=" * 60)
            print(result['result'])
        else:
            print(f"Error: {result.get('error')}", file=sys.stderr)
            sys.exit(1)


if __name__ == "__main__":
    main()
