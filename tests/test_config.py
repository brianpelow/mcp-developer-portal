"""Tests for PortalConfig."""

from mcpportal.core.config import PortalConfig


def test_config_defaults() -> None:
    config = PortalConfig()
    assert config.industry == "fintech"
    assert config.timeout_seconds == 30
    assert config.backstage_url == ""
    assert config.backstage_token == ""


def test_config_custom() -> None:
    config = PortalConfig(
        backstage_url="https://backstage.example.com",
        backstage_token="test-token",
        industry="manufacturing",
    )
    assert config.backstage_url == "https://backstage.example.com"
    assert config.industry == "manufacturing"


def test_has_backstage_false() -> None:
    config = PortalConfig(backstage_url="")
    assert config.has_backstage is False


def test_has_backstage_true() -> None:
    config = PortalConfig(backstage_url="https://backstage.example.com")
    assert config.has_backstage is True


def test_api_base() -> None:
    config = PortalConfig(backstage_url="https://backstage.example.com")
    assert config.api_base == "https://backstage.example.com/api"


def test_api_base_trailing_slash() -> None:
    config = PortalConfig(backstage_url="https://backstage.example.com/")
    assert config.api_base == "https://backstage.example.com/api"