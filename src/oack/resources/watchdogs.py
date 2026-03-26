"""Watchdog resource."""

from __future__ import annotations

import json
from typing import TYPE_CHECKING

from oack.types.watchdogs import CreateWatchdogParams, UpdateWatchdogParams, Watchdog

if TYPE_CHECKING:
    from oack._client import AsyncBaseClient, BaseClient


def _watchdog_path(account_id: str, page_id: str, comp_id: str) -> str:
    return f"/api/v1/accounts/{account_id}/status-pages/{page_id}/components/{comp_id}/watchdogs"


class AsyncWatchdogs:
    def __init__(self, client: AsyncBaseClient) -> None:
        self._client = client

    async def create(
        self, account_id: str, page_id: str, comp_id: str, params: CreateWatchdogParams
    ) -> Watchdog:
        resp = await self._client.request(
            "POST", _watchdog_path(account_id, page_id, comp_id), json=params.model_dump(exclude_none=True)
        )
        return Watchdog.model_validate_json(resp)

    async def list(self, account_id: str, page_id: str, comp_id: str) -> list[Watchdog]:
        resp = await self._client.request("GET", _watchdog_path(account_id, page_id, comp_id))
        return [Watchdog.model_validate(w) for w in json.loads(resp)]

    async def update(
        self, account_id: str, page_id: str, comp_id: str, watchdog_id: str, params: UpdateWatchdogParams
    ) -> Watchdog:
        resp = await self._client.request(
            "PUT",
            f"{_watchdog_path(account_id, page_id, comp_id)}/{watchdog_id}",
            json=params.model_dump(exclude_none=True),
        )
        return Watchdog.model_validate_json(resp)

    async def delete(self, account_id: str, page_id: str, comp_id: str, watchdog_id: str) -> None:
        await self._client.request("DELETE", f"{_watchdog_path(account_id, page_id, comp_id)}/{watchdog_id}")


class Watchdogs:
    def __init__(self, client: BaseClient) -> None:
        self._client = client

    def create(
        self, account_id: str, page_id: str, comp_id: str, params: CreateWatchdogParams
    ) -> Watchdog:
        resp = self._client.request(
            "POST", _watchdog_path(account_id, page_id, comp_id), json=params.model_dump(exclude_none=True)
        )
        return Watchdog.model_validate_json(resp)

    def list(self, account_id: str, page_id: str, comp_id: str) -> list[Watchdog]:
        resp = self._client.request("GET", _watchdog_path(account_id, page_id, comp_id))
        return [Watchdog.model_validate(w) for w in json.loads(resp)]

    def update(
        self, account_id: str, page_id: str, comp_id: str, watchdog_id: str, params: UpdateWatchdogParams
    ) -> Watchdog:
        resp = self._client.request(
            "PUT",
            f"{_watchdog_path(account_id, page_id, comp_id)}/{watchdog_id}",
            json=params.model_dump(exclude_none=True),
        )
        return Watchdog.model_validate_json(resp)

    def delete(self, account_id: str, page_id: str, comp_id: str, watchdog_id: str) -> None:
        self._client.request("DELETE", f"{_watchdog_path(account_id, page_id, comp_id)}/{watchdog_id}")
