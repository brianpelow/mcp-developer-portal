"""Tests for Backstage client."""

from mcpportal.clients.backstage import (
    BackstageClient,
    _mock_catalog,
    _mock_templates,
    _mock_techdocs,
)


def test_mock_catalog_returns_entities() -> None:
    client = BackstageClient(base_url="")
    entities = client.search_catalog()
    assert len(entities) > 0


def test_mock_catalog_filter_by_kind() -> None:
    client = BackstageClient(base_url="")
    entities = client.search_catalog(kind="Component")
    assert all(e.kind == "Component" for e in entities)


def test_mock_catalog_filter_by_query() -> None:
    client = BackstageClient(base_url="")
    entities = client.search_catalog(query="payments")
    assert len(entities) > 0
    assert any("payments" in e.name for e in entities)


def test_mock_templates_returned() -> None:
    client = BackstageClient(base_url="")
    templates = client.list_templates()
    assert len(templates) > 0
    assert any(t.name == "python-microservice" for t in templates)


def test_mock_techdocs_returned() -> None:
    client = BackstageClient(base_url="")
    docs = client.get_techdocs("Component", "default", "payments-service")
    assert len(docs) > 0
    assert "payments-service" in docs


def test_entity_has_required_fields() -> None:
    entities = _mock_catalog()
    for e in entities:
        assert e.kind
        assert e.name
        assert e.owner


def test_template_has_required_fields() -> None:
    templates = _mock_templates()
    for t in templates:
        assert t.name
        assert t.title
        assert t.description