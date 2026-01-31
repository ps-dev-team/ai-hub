#!/usr/bin/env python3
"""Export Figma artboards/frames as images for visual analysis."""

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


def find_top_frames(document, page_name=None):
    """Find top-level frames (artboards) in the file."""
    frames = []
    for page in document.get("children", []):
        if page.get("type") != "CANVAS":
            continue
        if page_name and page.get("name") != page_name:
            continue
        for child in page.get("children", []):
            if child.get("type") in ("FRAME", "COMPONENT", "COMPONENT_SET", "SECTION"):
                frames.append({
                    "id": child["id"],
                    "name": child.get("name", "Untitled"),
                    "page": page.get("name", ""),
                    "width": child.get("absoluteBoundingBox", {}).get("width"),
                    "height": child.get("absoluteBoundingBox", {}).get("height"),
                })
    return frames


def main():
    parser = argparse.ArgumentParser(description="Export Figma artboards as images")
    parser.add_argument("--file-key", required=True, help="Figma file key")
    parser.add_argument("--page", help="Filter by page name")
    parser.add_argument("--node-ids", help="Comma-separated node IDs (e.g., 1:2,1:3)")
    parser.add_argument("--format", default="png", choices=["png", "jpg", "svg", "pdf"])
    parser.add_argument("--scale", type=float, default=2, help="Export scale (1-4)")
    parser.add_argument("--out-dir", default="./figma-exports", help="Output directory")
    parser.add_argument("--list-only", action="store_true", help="List frames without exporting")
    args = parser.parse_args()

    token = get_token()
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    # Get file structure
    print(f"Fetching file {args.file_key}...")
    data = api_get(f"/v1/files/{args.file_key}?depth=2", token)
    print(f"File: {data.get('name', 'Unknown')}")

    if args.node_ids:
        node_ids = [nid.strip() for nid in args.node_ids.split(",")]
        frames = [{"id": nid, "name": nid} for nid in node_ids]
    else:
        frames = find_top_frames(data.get("document", {}), args.page)

    if not frames:
        print("No frames found.", file=sys.stderr)
        sys.exit(1)

    print(f"\nFound {len(frames)} frame(s):")
    for f in frames:
        size = f" ({f.get('width')}x{f.get('height')})" if f.get("width") else ""
        page = f" [{f.get('page')}]" if f.get("page") else ""
        print(f"  • {f['name']}{size}{page} (id: {f['id']})")

    if args.list_only:
        return

    # Export images
    ids = ",".join(f["id"] for f in frames)
    print(f"\nExporting {len(frames)} frame(s) as {args.format} @{args.scale}x...")
    images = api_get(
        f"/v1/images/{args.file_key}?ids={ids}&format={args.format}&scale={args.scale}",
        token,
    )

    id_to_name = {f["id"]: f["name"] for f in frames}
    exported = []
    for node_id, url in images.get("images", {}).items():
        if not url:
            print(f"  ✗ {id_to_name.get(node_id, node_id)} — render failed", file=sys.stderr)
            continue
        name = id_to_name.get(node_id, node_id).replace("/", "-").replace(" ", "-")
        filename = f"{name}.{args.format}"
        filepath = out_dir / filename
        urllib.request.urlretrieve(url, filepath)
        exported.append(str(filepath))
        print(f"  ✓ {filepath}")

    # Write manifest
    manifest = {"file_key": args.file_key, "file_name": data.get("name"), "exports": exported}
    manifest_path = out_dir / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2))
    print(f"\nDone! {len(exported)} images exported to {out_dir}/")


if __name__ == "__main__":
    main()
