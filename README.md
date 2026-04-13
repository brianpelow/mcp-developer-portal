# mcp-developer-portal

> MCP server wrapping Backstage — query service catalog, fetch TechDocs, and scaffold services via AI agents.

![CI](https://github.com/brianpelow/mcp-developer-portal/actions/workflows/ci.yml/badge.svg)
![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.12+-green.svg)
![MCP](https://img.shields.io/badge/MCP-compatible-purple.svg)

## Overview

`mcp-developer-portal` is a Model Context Protocol server that exposes your
Backstage internal developer portal to AI agents. It enables LLMs to query
the service catalog, fetch TechDocs documentation, look up ownership, explore
dependency graphs, and scaffold new services from golden-path templates.

Built for platform engineering teams in regulated financial services and
manufacturing who use Backstage as their engineering system of record.

## Tools exposed

| Tool | Description |
|------|-------------|
| `search_catalog` | Search the Backstage catalog by name, kind, or owner |
| `get_entity` | Get full details for a catalog entity |
| `get_techdocs` | Fetch TechDocs documentation for an entity |
| `get_ownership` | Look up who owns a service or component |
| `get_dependencies` | Get upstream and downstream dependencies |
| `scaffold_service` | Create a new service from a golden-path template |
| `list_templates` | List available scaffolding templates |

## Quick start

```bash
pip install mcp-developer-portal

export BACKSTAGE_URL=https://your-backstage.example.com
export BACKSTAGE_TOKEN=your_backstage_token

mcp-developer-portal
```

## Configuration

| Variable | Description | Required |
|----------|-------------|----------|
| `BACKSTAGE_URL` | Backstage instance URL | Yes |
| `BACKSTAGE_TOKEN` | Backstage API token | No |
| `PORTAL_INDUSTRY` | Industry context (fintech/manufacturing) | No |

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

Apache 2.0 — see [LICENSE](LICENSE).