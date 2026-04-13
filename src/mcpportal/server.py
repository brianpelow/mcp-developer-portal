"""FastMCP server entry point for mcp-developer-portal."""

from __future__ import annotations

import json
from mcpportal.core.config import PortalConfig
from mcpportal.tools.catalog import search_catalog, get_entity, get_ownership, get_dependencies
from mcpportal.tools.docs import get_techdocs, list_templates, scaffold_service


def create_server() -> object:
    """Create and configure the FastMCP server."""
    try:
        from fastmcp import FastMCP
    except ImportError:
        raise ImportError("fastmcp is required. Run: pip install fastmcp")

    config = PortalConfig.from_env()
    mcp = FastMCP(
        name="mcp-developer-portal",
        instructions=(
            "I provide access to your Backstage internal developer portal. "
            "I can search the service catalog, fetch TechDocs documentation, "
            "look up service ownership, explore dependency graphs, and scaffold "
            "new services from golden-path templates."
        ),
    )

    @mcp.tool()
    def search_catalog_tool(query: str = "", kind: str = "", owner: str = "") -> str:
        """Search the Backstage service catalog by name, kind, or owner."""
        return json.dumps(search_catalog(config, query=query, kind=kind, owner=owner), indent=2)

    @mcp.tool()
    def get_entity_tool(name: str, kind: str = "Component", namespace: str = "default") -> str:
        """Get full details for a catalog entity."""
        return json.dumps(get_entity(config, name=name, kind=kind, namespace=namespace), indent=2)

    @mcp.tool()
    def get_techdocs_tool(name: str, kind: str = "Component", namespace: str = "default") -> str:
        """Fetch TechDocs documentation for a catalog entity."""
        return json.dumps(get_techdocs(config, name=name, kind=kind, namespace=namespace), indent=2)

    @mcp.tool()
    def get_ownership_tool(name: str, kind: str = "Component") -> str:
        """Look up who owns a service or component."""
        return json.dumps(get_ownership(config, name=name, kind=kind), indent=2)

    @mcp.tool()
    def get_dependencies_tool(name: str, kind: str = "Component") -> str:
        """Get upstream and downstream dependencies for a service."""
        return json.dumps(get_dependencies(config, name=name, kind=kind), indent=2)

    @mcp.tool()
    def list_templates_tool() -> str:
        """List available golden-path scaffolding templates."""
        return json.dumps(list_templates(config), indent=2)

    @mcp.tool()
    def scaffold_service_tool(
        template_name: str,
        service_name: str,
        owner: str,
        description: str = "",
    ) -> str:
        """Scaffold a new service from a golden-path template."""
        return json.dumps(
            scaffold_service(config, template_name=template_name, service_name=service_name,
                           owner=owner, description=description), indent=2)

    return mcp


def main() -> None:
    """Entry point for the MCP server."""
    mcp = create_server()
    mcp.run()


if __name__ == "__main__":
    main()