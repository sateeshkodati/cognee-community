"""Offline cognee-1.5.x conformance tests. No ArcadeDB server, no secrets."""

import inspect

from cognee_community_hybrid_adapter_arcadedb.arcadedb_adapter import (
    ArcadeDBAdapter,
    ArcadeDBVectorAdapter,
)
from contract_suite import assert_graph_contract, assert_vector_contract
from contract_suite.graph_contract import assert_registered as graph_registered
from contract_suite.vector_contract import assert_registered as vector_registered

_SELF = object()


def _bind(method_name: str, *args, **kwargs) -> None:
    method = getattr(ArcadeDBAdapter, method_name)
    inspect.signature(method).bind(_SELF, *args, **kwargs)


def test_conforms_to_cognee_graph_contract():
    assert_graph_contract(ArcadeDBAdapter)


def test_conforms_to_cognee_vector_contract():
    assert_vector_contract(ArcadeDBVectorAdapter, instantiate=False)


def test_register_adds_arcadedb_providers():
    import cognee_community_hybrid_adapter_arcadedb.register  # noqa: F401

    graph_registered("arcadedb", ArcadeDBAdapter)
    vector_registered("arcadedb", ArcadeDBVectorAdapter)


def test_cognee_15_graph_call_shapes():
    _bind("add_node", "node-id", properties={"type": "Entity"})
    _bind(
        "add_edge",
        source_id="a",
        target_id="b",
        relationship_name="is_a",
        properties={"weight": 1},
    )
    _bind("has_edge", source_id="a", target_id="b", relationship_name="is_a")
    _bind("remove_belongs_to_set_tags", tags=["set-a"], node_ids=["node-id"])
    assert ArcadeDBAdapter.supports_cypher_queries is True


def test_graph_database_port_2480_is_http():
    adapter = ArcadeDBAdapter(
        graph_database_url="localhost",
        graph_database_port=2480,
    )
    assert adapter.http_base_url == "http://localhost:2480"


def test_graph_database_port_7687_does_not_override_http():
    adapter = ArcadeDBAdapter(
        graph_database_url="localhost",
        graph_database_port=7687,
    )
    assert adapter.http_base_url == "http://localhost:2480"
