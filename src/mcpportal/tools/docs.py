"""MCP tools for TechDocs and scaffolding."""

from __future__ import annotations

from mcpportal.clients.backstage import BackstageClient
from mcpportal.core.config import PortalConfig


def get_techdocs(config: PortalConfig, name: str, kind: str = "Component", namespace: str = "default") -> dict:
    """Fetch TechDocs documentation for a catalog entity."""
    client = BackstageClient(
        base_url=config.backstage_url,
        token=config.backstage_token,
        timeout=config.timeout_seconds,
    )
    content = client.get_techdocs(kind=kind, namespace=namespace, name=name)

    return {
        "source": "backstage_techdocs",
        "name": name,
        "kind": kind,
        "namespace": namespace,
        "content": content,
        "truncated": len(content) >= 5000,
    }


def list_templates(config: PortalConfig) -> dict:
    """List available golden-path scaffolding templates."""
    client = BackstageClient(
        base_url=config.backstage_url,
        token=config.backstage_token,
        timeout=config.timeout_seconds,
    )
    templates = client.list_templates()

    return {
        "source": "backstage",
        "count": len(templates),
        "templates": [
            {
                "name": t.name,
                "title": t.title,
                "description": t.description,
                "tags": t.tags,
                "owner": t.owner,
            }
            for t in templates
        ],
    }


def scaffold_service(
    config: PortalConfig,
    template_name: str,
    service_name: str,
    owner: str,
    description: str = "",
) -> dict:
    """Scaffold a new service from a golden-path template.

    Returns the scaffolding parameters that would be submitted to Backstage.
    In production, this calls the Backstage Scaffolder API.
    """
    client = BackstageClient(
        base_url=config.backstage_url,
        token=config.backstage_token,
        timeout=config.timeout_seconds,
    )
    templates = client.list_templates()
    template = next((t for t in templates if t.name == template_name), None)

    if not template:
        available = [t.name for t in templates]
        return {
            "error": f"Template '{template_name}' not found",
            "available_templates": available,
        }

    scaffold_params = {
        "templateRef": f"template:default/{template_name}",
        "values": {
            "name": service_name,
            "owner": owner,
            "description": description or f"A {config.industry} engineering service",
            "repoUrl": f"github.com?owner=brianpelow&repo={service_name}",
        },
    }

    return {
        "source": "backstage_scaffolder",
        "status": "ready",
        "template": template_name,
        "service_name": service_name,
        "owner": owner,
        "industry_context": config.industry,
        "scaffold_params": scaffold_params,
        "next_step": f"Submit to {config.backstage_url}/api/scaffolder/v2/tasks to create the service",
    }