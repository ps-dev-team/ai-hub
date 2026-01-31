---
name: youtube-gemini
description: Process and analyze YouTube videos using Gemini AI. Use when user shares a YouTube link and wants analysis, summary, transcription, or any insight from the video. Always ask what perspective or analysis they want before processing.
---

# YouTube Video Processor

Analyze YouTube videos using Gemini's video understanding capabilities.

## Setup

Set the `GEMINI_API_KEY` environment variable.

## Workflow

**IMPORTANT:** Always follow this workflow:

1. **User shares a YouTube URL** → Acknowledge receipt
2. **ASK what they want** → Before processing, always ask:
   - What kind of analysis do they need?
   - Any specific perspective? (developer, business, casual viewer, etc.)
   - Do they want a summary, key points, transcript, specific details?
3. **Build the prompt** → Create a clear prompt based on their request
4. **Process the video** → Run the script
5. **Return results in code blocks** → Easy to copy

## Usage

```bash
export GEMINI_API_KEY="your-key"
python scripts/process_video.py "<youtube_url>" "<prompt>"
```

### Arguments
- `url` — YouTube URL (any format) or video ID
- `prompt` — What to analyze/extract from the video
- `--json` / `-j` — Output raw JSON instead of formatted text

## Example Prompts

Based on user request, craft prompts like:

- **Summary:** "Summarize this video in 3-5 bullet points"
- **Developer perspective:** "Summarize the key technical insights from a software developer's perspective"
- **Key takeaways:** "What are the main actionable takeaways from this video?"
- **Transcript:** "Provide a detailed transcript of the spoken content"
- **Specific topic:** "What does the video say about [topic]?"

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
