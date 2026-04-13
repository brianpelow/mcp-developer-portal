"""Configuration for mcp-developer-portal."""

from __future__ import annotations

import os
from pydantic import BaseModel, Field


class PortalConfig(BaseModel):
    """Runtime configuration for the developer portal MCP server."""

    backstage_url: str = Field("", description="Backstage instance URL")
    backstage_token: str = Field("", description="Backstage API token")
    industry: str = Field("fintech", description="Industry context")
    timeout_seconds: int = Field(30, description="HTTP client timeout")
    use_mock: bool = Field(False, description="Use mock data when Backstage unavailable")

    @classmethod
    def from_env(cls) -> "PortalConfig":
        return cls(
            backstage_url=os.environ.get("BACKSTAGE_URL", ""),
            backstage_token=os.environ.get("BACKSTAGE_TOKEN", ""),
            industry=os.environ.get("PORTAL_INDUSTRY", "fintech"),
        )

    @property
    def has_backstage(self) -> bool:
        return bool(self.backstage_url)

    @property
    def api_base(self) -> str:
        return f"{self.backstage_url.rstrip('/')}/api"