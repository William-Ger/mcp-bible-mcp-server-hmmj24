# Bible MCP Server

A comprehensive Bible server providing verse lookup, search, chapter reading, and study tools using the Bible API

## MCP Server

This is a FastMCP server deployed on Railway.

### Tools
- `get_verse`: Look up specific Bible verses by reference (e.g., 'John 3:16', 'Romans 8:28')
- `search_verses`: Search for Bible verses containing specific words or phrases
- `get_chapter`: Get an entire Bible chapter
- `get_random_verse`: Get a random inspiring Bible verse

### Resources
- `bible://books`: List of all 66 books of the Bible with their abbreviations
- `bible://translations`: Available Bible translations and their codes

### Prompts
- `bible_study`: Generate a comprehensive Bible study guide for a given topic or passage
- `daily_reflection`: Create a daily devotional reflection based on a Bible verse or theme

## Usage

Add to your Claude Desktop config:

```json
{
  "mcpServers": {
    "bible-mcp-server": {
      "command": "npx",
      "args": ["-y", "mcp-remote", "YOUR_RAILWAY_URL/sse"]
    }
  }
}
```

---
Generated with MCP Builder
