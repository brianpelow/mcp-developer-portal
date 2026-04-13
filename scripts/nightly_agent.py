"""Nightly agent — automated maintenance for mcp-developer-portal."""

from __future__ import annotations

import json
import sys
from datetime import date, datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

REPO_ROOT = Path(__file__).parent.parent


def update_tool_manifest() -> None:
    """Write a manifest of all exposed MCP tools."""
    tools = [
        {"name": "search_catalog_tool", "source": "backstage", "description": "Search catalog by name, kind, owner"},
        {"name": "get_entity_tool", "source": "backstage", "description": "Get full entity details"},
        {"name": "get_techdocs_tool", "source": "backstage_techdocs", "description": "Fetch TechDocs content"},
        {"name": "get_ownership_tool", "source": "backstage", "description": "Look up service ownership"},
        {"name": "get_dependencies_tool", "source": "backstage", "description": "Get dependency graph"},
        {"name": "list_templates_tool", "source": "backstage", "description": "List scaffolding templates"},
        {"name": "scaffold_service_tool", "source": "backstage_scaffolder", "description": "Create service from template"},
    ]
    manifest = {
        "generated_at": datetime.utcnow().isoformat(),
        "date": date.today().isoformat(),
        "tool_count": len(tools),
        "tools": tools,
    }
    out = REPO_ROOT / "docs" / "tool-manifest.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(manifest, indent=2))
    print(f"[agent] Updated tool manifest -> {out}")


def update_mock_catalog_stats() -> None:
    """Write stats about the mock catalog for documentation."""
    from mcpportal.clients.backstage import _mock_catalog, _mock_templates
    entities = _mock_catalog()
    templates = _mock_templates()
    stats = {
        "generated_at": datetime.utcnow().isoformat(),
        "date": date.today().isoformat(),
        "mock_entity_count": len(entities),
        "mock_template_count": len(templates),
        "entity_kinds": list({e.kind for e in entities}),
        "template_names": [t.name for t in templates],
    }
    out = REPO_ROOT / "docs" / "catalog-stats.json"
    out.write_text(json.dumps(stats, indent=2))
    print(f"[agent] Updated catalog stats -> {out}")


def refresh_changelog() -> None:
    changelog = REPO_ROOT / "CHANGELOG.md"
    if not changelog.exists():
        return
    today = date.today().isoformat()
    content = changelog.read_text()
    if today not in content:
        content = content.replace("## [Unreleased]", f"## [Unreleased]\n\n_Last checked: {today}_", 1)
        changelog.write_text(content)
    print("[agent] Refreshed CHANGELOG timestamp")


if __name__ == "__main__":
    print(f"[agent] Starting nightly agent - {date.today().isoformat()}")
    update_tool_manifest()
    update_mock_catalog_stats()
    refresh_changelog()
    print("[agent] Done.")