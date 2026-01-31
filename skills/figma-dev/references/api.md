# Figma REST API Reference

Base URL: `https://api.figma.com`
Auth: `X-Figma-Token: <token>` header on every request.

## Files

### GET /v1/files/:key
Full file JSON. Use query params to limit scope:
- `depth=N` — tree depth (1=pages only, 2=pages+top-level objects)
- `ids=1:2,1:3` — only specific nodes + ancestors
- `geometry=paths` — include vector data

### GET /v1/files/:key/nodes?ids=1:2,1:3
Specific nodes and subtrees. Same optional params as above.

### GET /v1/images/:key
Render nodes as images.
- `ids=1:2,1:3` — nodes to render (required)
- `scale=1..4` — image scale (default 1)
- `format=jpg|png|svg|pdf` — output format (default png)

Returns `{ "images": { "1:2": "https://..." } }` — URLs expire after 30 days.

### GET /v1/files/:key/styles
Published styles in the file.

## Node Properties (key types)

All nodes have: `id`, `name`, `type`, `children` (if container).

### Common style properties
- `fills` — array of paint objects (solid, gradient, image)
- `strokes` — array of paint objects for borders
- `strokeWeight` — border width
- `cornerRadius` — border radius (or `rectangleCornerRadii` for individual corners)
- `effects` — shadows, blurs
- `opacity` — 0 to 1
- `blendMode`

### Layout (Auto Layout)
- `layoutMode` — `HORIZONTAL` | `VERTICAL` | `NONE`
- `primaryAxisAlignItems` — `MIN` | `CENTER` | `MAX` | `SPACE_BETWEEN`
- `counterAxisAlignItems` — `MIN` | `CENTER` | `MAX` | `BASELINE`
- `paddingLeft/Right/Top/Bottom`
- `itemSpacing` — gap between children
- `layoutSizingHorizontal/Vertical` — `FIXED` | `HUG` | `FILL`

### Text
- `characters` — the text content
- `style` — font properties:
  - `fontFamily`, `fontPostScriptName`
  - `fontSize`, `fontWeight`
  - `lineHeightPx`, `lineHeightPercent`
  - `letterSpacing`
  - `textAlignHorizontal` — `LEFT` | `CENTER` | `RIGHT` | `JUSTIFIED`
  - `textCase` — `ORIGINAL` | `UPPER` | `LOWER` | `TITLE`

### Color (in fills/strokes)
```json
{ "type": "SOLID", "color": { "r": 0.0-1.0, "g": 0.0-1.0, "b": 0.0-1.0, "a": 0.0-1.0 } }
```
Convert: `rgb(Math.round(r*255), Math.round(g*255), Math.round(b*255))`

### Dimensions
- `absoluteBoundingBox` — `{ x, y, width, height }` in absolute coords
- `size` — `{ x: width, y: height }` for vectors

### Component / Instance
- `componentId` — ID of the main component (on instances)
- `componentProperties` — variant props and values
- `overrides` — instance overrides

## Node Types
`DOCUMENT`, `CANVAS` (page), `FRAME`, `GROUP`, `SECTION`, `COMPONENT`, `COMPONENT_SET`, `INSTANCE`, `RECTANGLE`, `ELLIPSE`, `LINE`, `VECTOR`, `TEXT`, `BOOLEAN_OPERATION`, `SLICE`
