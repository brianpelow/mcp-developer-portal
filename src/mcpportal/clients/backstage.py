"""Backstage REST API client."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import httpx


@dataclass
class CatalogEntity:
    """A Backstage catalog entity."""

    kind: str
    name: str
    namespace: str
    description: str
    owner: str
    lifecycle: str
    tags: list[str] = field(default_factory=list)
    annotations: dict[str, str] = field(default_factory=dict)
    links: list[dict[str, str]] = field(default_factory=list)
    relations: list[dict[str, str]] = field(default_factory=list)


@dataclass
class ScaffoldTemplate:
    """A Backstage scaffolding template."""

    name: str
    title: str
    description: str
    tags: list[str] = field(default_factory=list)
    owner: str = ""


class BackstageClient:
    """Client for the Backstage Catalog and Scaffolder APIs."""

    def __init__(self, base_url: str, token: str = "", timeout: int = 30) -> None:
        self.base_url = base_url.rstrip("/")
        self.token = token
        self.timeout = timeout

    def _headers(self) -> dict[str, str]:
        headers = {"Content-Type": "application/json"}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers

    def search_catalog(self, query: str = "", kind: str = "", owner: str = "") -> list[CatalogEntity]:
        """Search the Backstage catalog."""
        if not self.base_url:
            return _mock_catalog(query=query, kind=kind)
        try:
            params: dict[str, Any] = {}
            filters = []
            if kind:
                filters.append(f"kind={kind}")
            if owner:
                filters.append(f"spec.owner={owner}")
            if filters:
                params["filter"] = ",".join(filters)
            with httpx.Client(timeout=self.timeout) as client:
                response = client.get(
                    f"{self.base_url}/api/catalog/entities",
                    headers=self._headers(),
                    params=params,
                )
                response.raise_for_status()
                entities = response.json()
                results = [_parse_entity(e) for e in entities]
                if query:
                    q = query.lower()
                    results = [e for e in results if q in e.name.lower() or q in e.description.lower()]
                return results
        except Exception:
            return _mock_catalog(query=query, kind=kind)

    def get_entity(self, kind: str, namespace: str, name: str) -> CatalogEntity | None:
        """Get a specific catalog entity by kind/namespace/name."""
        if not self.base_url:
            entities = _mock_catalog()
            return next((e for e in entities if e.name == name), None)
        try:
            with httpx.Client(timeout=self.timeout) as client:
                response = client.get(
                    f"{self.base_url}/api/catalog/entities/by-name/{kind}/{namespace}/{name}",
                    headers=self._headers(),
                )
                response.raise_for_status()
                return _parse_entity(response.json())
        except Exception:
            return None

    def get_techdocs(self, kind: str, namespace: str, name: str) -> str:
        """Fetch TechDocs content for an entity."""
        if not self.base_url:
            return _mock_techdocs(name)
        try:
            with httpx.Client(timeout=self.timeout) as client:
                response = client.get(
                    f"{self.base_url}/api/techdocs/static/docs/{namespace}/{kind}/{name}/index.html",
                    headers=self._headers(),
                )
                response.raise_for_status()
                return response.text[:5000]
        except Exception:
            return _mock_techdocs(name)

    def list_templates(self) -> list[ScaffoldTemplate]:
        """List available scaffolding templates."""
        if not self.base_url:
            return _mock_templates()
        try:
            with httpx.Client(timeout=self.timeout) as client:
                response = client.get(
                    f"{self.base_url}/api/catalog/entities",
                    headers=self._headers(),
                    params={"filter": "kind=Template"},
                )
                response.raise_for_status()
                return [_parse_template(e) for e in response.json()]
        except Exception:
            return _mock_templates()


def _parse_entity(data: dict[str, Any]) -> CatalogEntity:
    meta = data.get("metadata", {})
    spec = data.get("spec", {})
    return CatalogEntity(
        kind=data.get("kind", ""),
        name=meta.get("name", ""),
        namespace=meta.get("namespace", "default"),
        description=meta.get("description", ""),
        owner=spec.get("owner", ""),
        lifecycle=spec.get("lifecycle", ""),
        tags=meta.get("tags", []),
        annotations=meta.get("annotations", {}),
        relations=data.get("relations", []),
    )


def _parse_template(data: dict[str, Any]) -> ScaffoldTemplate:
    meta = data.get("metadata", {})
    spec = data.get("spec", {})
    return ScaffoldTemplate(
        name=meta.get("name", ""),
        title=spec.get("title", meta.get("name", "")),
        description=meta.get("description", ""),
        tags=meta.get("tags", []),
        owner=spec.get("owner", ""),
    )


def _mock_catalog(query: str = "", kind: str = "") -> list[CatalogEntity]:
    entities = [
        CatalogEntity(kind="Component", name="payments-service", namespace="default",
            description="ISO 20022 payment message processor", owner="payments-team",
            lifecycle="production", tags=["fintech", "payments", "sox-inscope"],
            annotations={"github.com/project-slug": "org/payments-service"},
            relations=[{"type": "dependsOn", "targetRef": "component:default/fx-rate-service"}]),
        CatalogEntity(kind="Component", name="fx-rate-service", namespace="default",
            description="Real-time FX rate aggregation service", owner="trading-team",
            lifecycle="production", tags=["fintech", "trading"],
            annotations={"github.com/project-slug": "org/fx-rate-service"}, relations=[]),
        CatalogEntity(kind="Component", name="audit-service", namespace="default",
            description="Immutable audit trail service for SOX compliance", owner="platform-team",
            lifecycle="production", tags=["fintech", "compliance", "sox"],
            annotations={"github.com/project-slug": "org/audit-service"}, relations=[]),
        CatalogEntity(kind="API", name="payments-api", namespace="default",
            description="Payments REST API — OpenAPI 3.0", owner="payments-team",
            lifecycle="production", tags=["api", "openapi"], annotations={}, relations=[]),
        CatalogEntity(kind="System", name="trading-platform", namespace="default",
            description="Core trading and payments platform", owner="platform-team",
            lifecycle="production", tags=["fintech", "platform"], annotations={}, relations=[]),
    ]
    if query:
        q = query.lower()
        entities = [e for e in entities if q in e.name.lower() or q in e.description.lower()]
    if kind:
        entities = [e for e in entities if e.kind.lower() == kind.lower()]
    return entities


def _mock_techdocs(name: str) -> str:
    return f"""# {name} — Technical Documentation

## Overview
This service is part of the regulated financial services platform.

## Architecture
The service follows a hexagonal architecture pattern with clear separation
between domain logic and infrastructure adapters.

## Getting started
See the README for local development setup instructions.

## API reference
Full API documentation is available in the Backstage API catalog.

## Operations
Runbooks are maintained in the runbook-gen repository.
On-call procedures are documented in PagerDuty.

## Compliance
This service is subject to SOX ITGC controls and PCI-DSS requirements.
All changes require peer review and automated testing before deployment.
"""


def _mock_templates() -> list[ScaffoldTemplate]:
    return [
        ScaffoldTemplate(name="python-microservice", title="Python Microservice",
            description="FastAPI service with uv, tests, CI/CD, and compliance artifacts",
            tags=["python", "fastapi", "fintech"], owner="platform-team"),
        ScaffoldTemplate(name="typescript-dashboard", title="TypeScript Dashboard",
            description="Next.js dashboard with Tailwind, Vitest, and Backstage integration",
            tags=["typescript", "nextjs"], owner="platform-team"),
        ScaffoldTemplate(name="mcp-server", title="MCP Server",
            description="Model Context Protocol server with FastMCP and typed tools",
            tags=["python", "mcp", "ai-agents"], owner="platform-team"),
    ]