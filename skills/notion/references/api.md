# Notion API Reference

Base URL: `https://api.notion.com/v1`

## Authentication

All requests need:
```
Authorization: Bearer $NOTION_API_KEY
Notion-Version: 2022-06-28
Content-Type: application/json
```

## Pages

### Get page

```
GET /pages/{page_id}
```

### Create page

```
POST /pages
```

```json
{
  "parent": {"database_id": "xxx"},
  "properties": {
    "Name": {"title": [{"text": {"content": "New Item"}}]},
    "Status": {"select": {"name": "Todo"}}
  }
}
```

### Update page properties

```
PATCH /pages/{page_id}
```

```json
{
  "properties": {
    "Status": {"select": {"name": "Done"}},
    "Completed At": {"date": {"start": "2025-01-31T18:00:00.000Z"}}
  }
}
```

## Databases

### Query a database

```
POST /databases/{database_id}/query
```

```json
{
  "filter": {
    "property": "Status",
    "select": {"equals": "In Progress"}
  },
  "sorts": [
    {"property": "Priority", "direction": "ascending"}
  ]
}
```

#### Compound filters

```json
{
  "filter": {
    "and": [
      {"property": "Status", "select": {"equals": "In Progress"}},
      {"property": "Project", "select": {"equals": "video-editor-ps"}}
    ]
  }
}
```

### Create a database

```
POST /databases
```

```json
{
  "parent": {"page_id": "xxx"},
  "title": [{"text": {"content": "My Database"}}],
  "properties": {
    "Name": {"title": {}},
    "Status": {"select": {"options": [{"name": "Todo"}, {"name": "Done"}]}},
    "Date": {"date": {}}
  }
}
```

## Blocks

### Get page content

```
GET /blocks/{page_id}/children
```

### Append blocks

```
PATCH /blocks/{page_id}/children
```

```json
{
  "children": [
    {
      "object": "block",
      "type": "paragraph",
      "paragraph": {
        "rich_text": [{"text": {"content": "Hello world"}}]
      }
    }
  ]
}
```

## Search

```
POST /search
```

```json
{
  "query": "page title",
  "filter": {"property": "object", "value": "page"}
}
```

## Property Types

Formats for setting properties on pages:

| Type | Format |
|---|---|
| Title | `{"title": [{"text": {"content": "..."}}]}` |
| Rich text | `{"rich_text": [{"text": {"content": "..."}}]}` |
| Select | `{"select": {"name": "Option"}}` |
| Multi-select | `{"multi_select": [{"name": "A"}, {"name": "B"}]}` |
| Date | `{"date": {"start": "2025-01-15"}}` |
| Date range | `{"date": {"start": "2025-01-15", "end": "2025-01-16"}}` |
| Datetime | `{"date": {"start": "2025-01-15T10:00:00.000Z"}}` |
| Checkbox | `{"checkbox": true}` |
| Number | `{"number": 42}` |
| URL | `{"url": "https://..."}` |
| Email | `{"email": "a@b.com"}` |
| Relation | `{"relation": [{"id": "page_id"}]}` |

## Filter Operators

| Property Type | Operators |
|---|---|
| Select | `equals`, `does_not_equal`, `is_empty`, `is_not_empty` |
| Text/Title | `equals`, `contains`, `starts_with`, `ends_with`, `is_empty`, `is_not_empty` |
| Number | `equals`, `greater_than`, `less_than`, `greater_than_or_equal_to`, `less_than_or_equal_to` |
| Date | `equals`, `before`, `after`, `on_or_before`, `on_or_after`, `is_empty`, `is_not_empty` |
| Checkbox | `equals` |

## Notes

- Page/database IDs are UUIDs (with or without dashes)
- Rate limit: ~3 requests/second average
- Database views and filters are UI-only (cannot be set via API)
- Maximum 100 results per query (use `start_cursor` for pagination)
