"""MCP tools for Backstage catalog queries."""

from __future__ import annotations

from mcpportal.clients.backstage import BackstageClient
from mcpportal.core.config import PortalConfig


def search_catalog(config: PortalConfig, query: str = "", kind: str = "", owner: str = "") -> dict:
    """Search the Backstage service catalog."""
    client = BackstageClient(
        base_url=config.backstage_url,
        token=config.backstage_token,
        timeout=config.timeout_seconds,
    )
    entities = client.search_catalog(query=query, kind=kind, owner=owner)

    return {
        "source": "backstage",
        "count": len(entities),
        "query": query or "*",
        "kind_filter": kind or "all",
        "entities": [
            {
                "kind": e.kind,
                "name": e.name,
                "namespace": e.namespace,
                "description": e.description,
                "owner": e.owner,
                "lifecycle": e.lifecycle,
                "tags": e.tags,
            }
            for e in entities
        ],
    }


def get_entity(config: PortalConfig, name: str, kind: str = "Component", namespace: str = "default") -> dict:
    """Get full details for a catalog entity."""
    client = BackstageClient(
        base_url=config.backstage_url,
        token=config.backstage_token,
        timeout=config.timeout_seconds,
    )
    entity = client.get_entity(kind=kind, namespace=namespace, name=name)

    if not entity:
        return {"error": f"Entity not found: {kind}/{namespace}/{name}"}

    return {
        "source": "backstage",
        "kind": entity.kind,
        "name": entity.name,
        "namespace": entity.namespace,
        "description": entity.description,
        "owner": entity.owner,
        "lifecycle": entity.lifecycle,
        "tags": entity.tags,
        "annotations": entity.annotations,
        "relations": entity.relations,
    }


def get_ownership(config: PortalConfig, name: str, kind: str = "Component") -> dict:
    """Look up who owns a service or component."""
    client = BackstageClient(
        base_url=config.backstage_url,
        token=config.backstage_token,
        timeout=config.timeout_seconds,
    )
    entity = client.get_entity(kind=kind, namespace="default", name=name)

    if not entity:
        return {"error": f"Entity not found: {name}"}

    github_slug = entity.annotations.get("github.com/project-slug", "")
    pagerduty = entity.annotations.get("pagerduty.com/service-id", "")

    return {
        "source": "backstage",
        "name": name,
        "kind": kind,
        "owner": entity.owner,
        "lifecycle": entity.lifecycle,
        "github_slug": github_slug,
        "pagerduty_service_id": pagerduty,
        "tags": entity.tags,
    }


def get_dependencies(config: PortalConfig, name: str, kind: str = "Component") -> dict:
    """Get upstream and downstream dependencies for a service."""
    client = BackstageClient(
        base_url=config.backstage_url,
        token=config.backstage_token,
        timeout=config.timeout_seconds,
    )
    entity = client.get_entity(kind=kind, namespace="default", name=name)

    if not entity:
        return {"error": f"Entity not found: {name}"}

    depends_on = [
        r.get("targetRef", "") for r in entity.relations
        if r.get("type") == "dependsOn"
    ]
    depended_on_by = [
        r.get("targetRef", "") for r in entity.relations
        if r.get("type") == "dependencyOf"
    ]

    return {
        "source": "backstage",
        "name": name,
        "kind": kind,
        "depends_on": depends_on,
        "depended_on_by": depended_on_by,
        "total_dependencies": len(depends_on) + len(depended_on_by),
    }