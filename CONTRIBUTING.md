# Contributing

## Development setup

```bash
git clone https://github.com/brianpelow/mcp-developer-portal
cd mcp-developer-portal
uv sync
uv run pytest
```

## Running the MCP server locally

```bash
export BACKSTAGE_URL=https://your-backstage.example.com
export BACKSTAGE_TOKEN=your_token
uv run mcp-developer-portal
```

## Standards

- All PRs require passing CI
- Test coverage must not decrease
- Update CHANGELOG.md for user-facing changes