"""Tests for MCP tool functions."""

from mcpportal.core.config import PortalConfig
from mcpportal.tools.catalog import search_catalog, get_entity, get_ownership, get_dependencies
from mcpportal.tools.docs import get_techdocs, list_templates, scaffold_service


def make_config(**kwargs) -> PortalConfig:
    return PortalConfig(**kwargs)


def test_search_catalog_returns_results() -> None:
    config = make_config()
    result = search_catalog(config)
    assert "entities" in result
    assert result["count"] > 0
    assert result["source"] == "backstage"


def test_search_catalog_with_query() -> None:
    config = make_config()
    result = search_catalog(config, query="payments")
    assert "entities" in result
    assert result["count"] > 0
    assert any("payments" in e["name"] for e in result["entities"])


def test_search_catalog_with_kind() -> None:
    config = make_config()
    result = search_catalog(config, kind="Component")
    assert all(e["kind"] == "Component" for e in result["entities"])


def test_get_entity_found() -> None:
    config = make_config()
    result = get_entity(config, name="payments-service")
    assert "error" not in result
    assert result["name"] == "payments-service"


def test_get_entity_not_found() -> None:
    config = make_config()
    result = get_entity(config, name="nonexistent-service")
    assert "error" in result


def test_get_ownership_returns_owner() -> None:
    config = make_config()
    result = get_ownership(config, name="payments-service")
    assert "owner" in result
    assert result["owner"] == "payments-team"


def test_get_dependencies_returns_relations() -> None:
    config = make_config()
    result = get_dependencies(config, name="payments-service")
    assert "depends_on" in result
    assert "depended_on_by" in result
    assert "total_dependencies" in result


def test_get_techdocs_returns_content() -> None:
    config = make_config()
    result = get_techdocs(config, name="payments-service")
    assert "content" in result
    assert len(result["content"]) > 0
    assert result["source"] == "backstage_techdocs"


def test_list_templates_returns_templates() -> None:
    config = make_config()
    result = list_templates(config)
    assert "templates" in result
    assert result["count"] > 0


def test_scaffold_service_valid_template() -> None:
    config = make_config()
    result = scaffold_service(
        config,
        template_name="python-microservice",
        service_name="new-payments-api",
        owner="payments-team",
        description="New payments API service",
    )
    assert "error" not in result
    assert result["service_name"] == "new-payments-api"
    assert result["status"] == "ready"


def test_scaffold_service_invalid_template() -> None:
    config = make_config()
    result = scaffold_service(
        config,
        template_name="nonexistent-template",
        service_name="my-service",
        owner="my-team",
    )
    assert "error" in result
    assert "available_templates" in result