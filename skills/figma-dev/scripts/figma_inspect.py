#!/usr/bin/env python3
"""Inspect specific Figma nodes — extract detailed properties for implementation."""

import argparse
import json
import os
import sys
import urllib.request
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


def extract_css_props(node):
    """Extract CSS-relevant properties from a node."""
    css = {}
    ntype = node.get("type", "")

    # Dimensions
    bb = node.get("absoluteBoundingBox", {})
    if bb:
        css["width"] = f"{bb.get('width', 0)}px"
        css["height"] = f"{bb.get('height', 0)}px"

    # Background / fills
    fills = [f for f in node.get("fills", []) if f.get("visible", True)]
    if fills and fills[0].get("type") == "SOLID":
        css["background"] = color_to_hex(fills[0]["color"])

    # Border
    strokes = [s for s in node.get("strokes", []) if s.get("visible", True)]
    if strokes and strokes[0].get("type") == "SOLID":
        weight = node.get("strokeWeight", 1)
        color = color_to_hex(strokes[0]["color"])
        css["border"] = f"{weight}px solid {color}"

    # Border radius
    cr = node.get("cornerRadius")
    if cr:
        css["borderRadius"] = f"{cr}px"
    elif node.get("rectangleCornerRadii"):
        tl, tr, br, bl = node["rectangleCornerRadii"]
        css["borderRadius"] = f"{tl}px {tr}px {br}px {bl}px"

    # Opacity
    opacity = node.get("opacity")
    if opacity is not None and opacity < 1:
        css["opacity"] = f"{opacity}"

    # Layout (auto-layout → flexbox)
    layout_mode = node.get("layoutMode")
    if layout_mode and layout_mode != "NONE":
        css["display"] = "flex"
        css["flexDirection"] = "row" if layout_mode == "HORIZONTAL" else "column"

        align_map = {"MIN": "flex-start", "CENTER": "center", "MAX": "flex-end", "SPACE_BETWEEN": "space-between"}
        primary = node.get("primaryAxisAlignItems", "MIN")
        counter = node.get("counterAxisAlignItems", "MIN")
        css["justifyContent"] = align_map.get(primary, primary)
        css["alignItems"] = align_map.get(counter, counter)

        gap = node.get("itemSpacing")
        if gap:
            css["gap"] = f"{gap}px"

    # Padding
    paddings = {}
    for side in ("Top", "Right", "Bottom", "Left"):
        val = node.get(f"padding{side}")
        if val:
            paddings[side.lower()] = val
    if paddings:
        vals = [paddings.get(s, 0) for s in ("top", "right", "bottom", "left")]
        css["padding"] = " ".join(f"{v}px" for v in vals)

    # Typography
    style = node.get("style", {})
    if style.get("fontFamily"):
        css["fontFamily"] = style["fontFamily"]
        css["fontSize"] = f"{style.get('fontSize', 16)}px"
        css["fontWeight"] = str(style.get("fontWeight", 400))
        lh = style.get("lineHeightPx")
        if lh:
            css["lineHeight"] = f"{lh}px"
        ls = style.get("letterSpacing")
        if ls:
            css["letterSpacing"] = f"{ls}px"
        align = style.get("textAlignHorizontal", "LEFT").lower()
        if align != "left":
            css["textAlign"] = align

    # Text color (from fills on text nodes)
    if ntype == "TEXT" and fills:
        css["color"] = css.pop("background", None) or color_to_hex(fills[0].get("color", {}))

    # Effects (shadows)
    for effect in node.get("effects", []):
        if not effect.get("visible", True):
            continue
        if effect["type"] == "DROP_SHADOW":
            o = effect.get("offset", {})
            r = effect.get("radius", 0)
            c = color_to_hex(effect["color"]) if "color" in effect else "rgba(0,0,0,0.25)"
            css["boxShadow"] = f"{o.get('x', 0)}px {o.get('y', 0)}px {r}px {c}"

    return {k: v for k, v in css.items() if v is not None}


def summarize_node(node, depth=0, max_depth=3):
    """Create a developer-friendly summary of a node tree."""
    if depth > max_depth:
        return None

    summary = {
        "name": node.get("name"),
        "type": node.get("type"),
        "css": extract_css_props(node),
    }

    if node.get("type") == "TEXT":
        summary["text"] = node.get("characters", "")

    if node.get("type") == "INSTANCE":
        summary["componentId"] = node.get("componentId")

    children = node.get("children", [])
    if children:
        child_summaries = [summarize_node(c, depth + 1, max_depth) for c in children]
        summary["children"] = [c for c in child_summaries if c]

    return summary


def main():
    parser = argparse.ArgumentParser(description="Inspect Figma nodes for implementation")
    parser.add_argument("--file-key", required=True, help="Figma file key")
    parser.add_argument("--node-ids", required=True, help="Comma-separated node IDs")
    parser.add_argument("--depth", type=int, default=4, help="Max tree depth")
    parser.add_argument("--out", help="Output file (default: stdout)")
    parser.add_argument("--raw", action="store_true", help="Output raw Figma JSON instead of summary")
    args = parser.parse_args()

    token = get_token()
    ids = args.node_ids.replace("-", ":")

    print(f"Inspecting nodes: {ids}", file=sys.stderr)
    data = api_get(f"/v1/files/{args.file_key}/nodes?ids={ids}", token)

    if args.raw:
        result = data.get("nodes", {})
    else:
        result = {}
        for node_id, node_data in data.get("nodes", {}).items():
            if node_data and node_data.get("document"):
                result[node_id] = summarize_node(node_data["document"], max_depth=args.depth)

    output = json.dumps(result, indent=2)

    if args.out:
        Path(args.out).write_text(output)
        print(f"Written to {args.out}", file=sys.stderr)
    else:
        print(output)


if __name__ == "__main__":
    main()
