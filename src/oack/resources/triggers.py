"""Trigger resource."""

from __future__ import annotations

import json
from typing import TYPE_CHECKING

from oack.types.triggers import CreateTriggerParams, Trigger, UpdateTriggerParams

if TYPE_CHECKING:
    from oack._client import AsyncBaseClient, BaseClient


def _trigger_path(account_id: str, page_id: str, comp_id: str) -> str:
    return f"/api/v1/accounts/{account_id}/status-pages/{page_id}/components/{comp_id}/triggers"


class AsyncTriggers:
    def __init__(self, client: AsyncBaseClient) -> None:
        self._client = client

    async def create(self, account_id: str, page_id: str, comp_id: str, params: CreateTriggerParams) -> Trigger:
        resp = await self._client.request(
            "POST", _trigger_path(account_id, page_id, comp_id), json=params.model_dump(exclude_none=True)
        )
        return Trigger.model_validate_json(resp)

    async def list(self, account_id: str, page_id: str, comp_id: str) -> list[Trigger]:
        resp = await self._client.request("GET", _trigger_path(account_id, page_id, comp_id))
        return [Trigger.model_validate(t) for t in json.loads(resp)]

    async def update(
        self, account_id: str, page_id: str, comp_id: str, trigger_id: str, params: UpdateTriggerParams
    ) -> Trigger:
        resp = await self._client.request(
            "PUT",
            f"{_trigger_path(account_id, page_id, comp_id)}/{trigger_id}",
            json=params.model_dump(exclude_none=True),
        )
        return Trigger.model_validate_json(resp)

    async def delete(self, account_id: str, page_id: str, comp_id: str, trigger_id: str) -> None:
        await self._client.request("DELETE", f"{_trigger_path(account_id, page_id, comp_id)}/{trigger_id}")


class Triggers:
    def __init__(self, client: BaseClient) -> None:
        self._client = client

    def create(self, account_id: str, page_id: str, comp_id: str, params: CreateTriggerParams) -> Trigger:
        resp = self._client.request(
            "POST", _trigger_path(account_id, page_id, comp_id), json=params.model_dump(exclude_none=True)
        )
        return Trigger.model_validate_json(resp)

    def list(self, account_id: str, page_id: str, comp_id: str) -> list[Trigger]:
        resp = self._client.request("GET", _trigger_path(account_id, page_id, comp_id))
        return [Trigger.model_validate(t) for t in json.loads(resp)]

    def update(
        self, account_id: str, page_id: str, comp_id: str, trigger_id: str, params: UpdateTriggerParams
    ) -> Trigger:
        resp = self._client.request(
            "PUT",
            f"{_trigger_path(account_id, page_id, comp_id)}/{trigger_id}",
            json=params.model_dump(exclude_none=True),
        )
        return Trigger.model_validate_json(resp)

    def delete(self, account_id: str, page_id: str, comp_id: str, trigger_id: str) -> None:
        self._client.request("DELETE", f"{_trigger_path(account_id, page_id, comp_id)}/{trigger_id}")
