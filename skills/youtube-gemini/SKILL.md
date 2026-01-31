---
name: youtube-gemini
description: Process and analyze YouTube videos using Gemini AI. Use when user shares a YouTube link and wants analysis, summary, transcription, or any insight from the video. Present numbered analysis options before processing.
---

# YouTube Video Processor

Analyze YouTube videos using Gemini's video understanding capabilities.

## Setup

Set the `GEMINI_API_KEY` environment variable.

## Workflow

1. **User shares a YouTube URL** → Acknowledge receipt
2. **Present analysis options** → Always show the numbered list below
3. **User picks a number (or describes custom)** → Build the prompt
4. **Process the video** → Run the script
5. **Return results** → Format based on the chosen analysis type

## Analysis Options

Always present these options when a user shares a YouTube link:

```
1. Notes & Summary — Bullet points of all key topics + concise narrative summary from the speaker's perspective
2. Quick Summary — 3-5 bullet points, main takeaways only
3. Deep Dive — Detailed analysis of concepts, arguments, and structure
4. Action Items — Practical takeaways and next steps
5. Content Repurpose — Hooks, quotes, and ideas for social media posts
6. Transcript — Full spoken content transcription
7. Other — Custom analysis (describe what you need)
```

### Prompts per Option

Use these prompts when processing:

**1 — Notes & Summary:**
"Analyze this video and provide: (A) A comprehensive list of bullet points covering every notable topic, insight, and detail mentioned. (B) A concise narrative summary written from the speaker's perspective, staying faithful to their message and tone. Keep it easy to understand while being as complete as possible."

**2 — Quick Summary:**
"Summarize this video in 3-5 bullet points covering only the main takeaways."

**3 — Deep Dive:**
"Provide a detailed analysis of this video: main arguments, supporting evidence, structure, key concepts, and any notable quotes or data points mentioned."

**4 — Action Items:**
"Extract all practical, actionable takeaways from this video. Format as a numbered list of concrete next steps someone could implement."

**5 — Content Repurpose:**
"Extract content repurposing material from this video: (A) 3-5 strong hooks or opening lines. (B) Memorable quotes. (C) Key statistics or data points. (D) 3-5 social media post ideas based on the video's content."

**6 — Transcript:**
"Provide a detailed transcription of all spoken content in this video."

**7 — Other:**
Use the user's custom prompt directly.

## Usage

```bash
export GEMINI_API_KEY="your-key"
python scripts/process_video.py "<youtube_url>" "<prompt>"
```

### Arguments
- `url` — YouTube URL (any format) or video ID
- `prompt` — What to analyze/extract from the video
- `--json` / `-j` — Output raw JSON instead of formatted text

## Supported URL Formats

- `https://www.youtube.com/watch?v=VIDEO_ID`
- `https://youtu.be/VIDEO_ID`
- `https://youtube.com/shorts/VIDEO_ID`
- `https://youtube.com/embed/VIDEO_ID`
- Just the video ID directly

## Dependencies

Requires `google-genai` package:
```bash
pip install google-genai
```
