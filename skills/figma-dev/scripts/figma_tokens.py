#!/usr/bin/env python3
"""Extract design tokens (colors, fonts, spacing, effects) from a Figma file."""

import argparse
import json
import os
import sys
import urllib.request
from collections import defaultdict
from pathlib import Path


def get_token():
    """Get Figma API token from environment variables."""
    token = os.environ.get("FIGMA_API_TOKEN") or os.environ.get("FIGMA_TOKEN")
    if token:
        return token
    print("Error: No Figma token found. Set FIGMA_API_TOKEN environment variable.", file=sys.stderr)
    sys.exit(1)


def api_get(endpoint, token):
    url = f"https://api.figma.com{endpoint}"
    req = urllib.request.Request(url, headers={"X-Figma-Token": token})
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read())


def color_to_hex(c):
    r, g, b = int(c["r"] * 255), int(c["g"] * 255), int(c["b"] * 255)
    a = c.get("a", 1)
    if a < 1:
        return f"rgba({r}, {g}, {b}, {a:.2f})"
    return f"#{r:02x}{g:02x}{b:02x}"


def walk_nodes(node, visitor, depth=0):
    visitor(node, depth)
    for child in node.get("children", []):
        walk_nodes(child, visitor, depth + 1)


def extract_tokens(document):
    colors = defaultdict(int)
    fonts = defaultdict(int)
    font_sizes = defaultdict(int)
    spacings = defaultdict(int)
    radii = defaultdict(int)
    effects_list = []

    def visit(node, depth):
        # Colors from fills
        for fill in node.get("fills", []):
            if fill.get("type") == "SOLID" and fill.get("visible", True):
                c = fill.get("color", {})
                hex_val = color_to_hex(c)
                colors[hex_val] += 1

        # Colors from strokes
        for stroke in node.get("strokes", []):
            if stroke.get("type") == "SOLID" and stroke.get("visible", True):
                c = stroke.get("color", {})
                hex_val = color_to_hex(c)
                colors[hex_val] += 1

        # Typography
        style = node.get("style", {})
        if style.get("fontFamily"):
            font_key = f"{style['fontFamily']} {style.get('fontWeight', 400)}"
            fonts[font_key] += 1
        if style.get("fontSize"):
            font_sizes[int(style["fontSize"])] += 1

        # Spacing (auto-layout)
        if node.get("itemSpacing") is not None:
            spacings[int(node["itemSpacing"])] += 1
        for prop in ("paddingLeft", "paddingRight", "paddingTop", "paddingBottom"):
            val = node.get(prop)
            if val is not None and val > 0:
                spacings[int(val)] += 1

        # Border radius
        cr = node.get("cornerRadius")
        if cr is not None and cr > 0:
            radii[int(cr)] += 1

        # Effects
        for effect in node.get("effects", []):
            if effect.get("visible", True):
                effects_list.append({
                    "type": effect.get("type"),
                    "radius": effect.get("radius"),
                    "offset": effect.get("offset"),
                    "color": color_to_hex(effect["color"]) if "color" in effect else None,
                })

    walk_nodes(document, visit)

    return {
        "colors": dict(sorted(colors.items(), key=lambda x: -x[1])),
        "fonts": dict(sorted(fonts.items(), key=lambda x: -x[1])),
        "fontSizes": dict(sorted(font_sizes.items())),
        "spacing": dict(sorted(spacings.items())),
        "borderRadii": dict(sorted(radii.items())),
        "effects": effects_list[:20],
    }


def main():
    parser = argparse.ArgumentParser(description="Extract design tokens from Figma")
    parser.add_argument("--file-key", required=True, help="Figma file key")
    parser.add_argument("--page", help="Filter by page name")
    parser.add_argument("--out", default="./figma-tokens.json", help="Output file")
    args = parser.parse_args()

    token = get_token()

    print(f"Fetching file {args.file_key}...")
    data = api_get(f"/v1/files/{args.file_key}", token)
    print(f"File: {data.get('name', 'Unknown')}")

    doc = data.get("document", {})
    if args.page:
        for page in doc.get("children", []):
            if page.get("name") == args.page:
                doc = page
                break

    print("Extracting tokens...")
    tokens = extract_tokens(doc)

    # Also extract styles
    styles = data.get("styles", {})
    if styles:
        tokens["publishedStyles"] = {
            sid: {"name": s.get("name"), "type": s.get("style_type")}
            for sid, s in styles.items()
        }

    out_path = Path(args.out)
    out_path.write_text(json.dumps(tokens, indent=2))
    print(f"\nTokens extracted to {out_path}")
    print(f"  Colors: {len(tokens['colors'])}")
    print(f"  Fonts: {len(tokens['fonts'])}")
    print(f"  Font sizes: {len(tokens['fontSizes'])}")
    print(f"  Spacing values: {len(tokens['spacing'])}")
    print(f"  Border radii: {len(tokens['borderRadii'])}")
    print(f"  Effects: {len(tokens['effects'])}")
    if tokens.get("publishedStyles"):
        print(f"  Published styles: {len(tokens['publishedStyles'])}")


if __name__ == "__main__":
    main()
