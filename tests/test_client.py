"""Smoke tests for client construction."""

from oack import AsyncOack, Oack


def test_sync_client_init() -> None:
    client = Oack(api_key="sk-test")
    assert client.monitors is not None
    assert client.teams is not None
    client.close()


def test_async_client_init() -> None:
    client = AsyncOack(api_key="sk-test")
    assert client.monitors is not None
    assert client.teams is not None
