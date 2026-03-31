"""Service resource."""

from __future__ import annotations

import json
from typing import TYPE_CHECKING

from oack.types.services import CreateServiceParams, Service, ServiceAnalytics, UpdateServiceParams

if TYPE_CHECKING:
    from oack._client import AsyncBaseClient, BaseClient


def _base_path(account_id: str) -> str:
    return f"/api/v1/accounts/{account_id}/services"


def _service_path(account_id: str, service_id: str) -> str:
    return f"{_base_path(account_id)}/{service_id}"


class AsyncServices:
    def __init__(self, client: AsyncBaseClient) -> None:
        self._client = client

    async def create(self, account_id: str, params: CreateServiceParams) -> Service:
        resp = await self._client.request("POST", _base_path(account_id), json=params.model_dump(exclude_none=True))
        return Service.model_validate_json(resp)

    async def list(self, account_id: str) -> list[Service]:
        resp = await self._client.request("GET", _base_path(account_id))
        return [Service.model_validate(s) for s in json.loads(resp)]

    async def get(self, account_id: str, service_id: str) -> Service:
        resp = await self._client.request("GET", _service_path(account_id, service_id))
        return Service.model_validate_json(resp)

    async def update(self, account_id: str, service_id: str, params: UpdateServiceParams) -> Service:
        resp = await self._client.request(
            "PUT", _service_path(account_id, service_id), json=params.model_dump(exclude_none=True)
        )
        return Service.model_validate_json(resp)

    async def delete(self, account_id: str, service_id: str) -> None:
        await self._client.request("DELETE", _service_path(account_id, service_id))

    async def link_monitors(self, account_id: str, service_id: str, monitor_ids: list[str]) -> None:
        await self._client.request(
            "POST",
            f"{_service_path(account_id, service_id)}/monitors",
            json={"monitor_ids": monitor_ids},
        )

    async def unlink_monitor(self, account_id: str, service_id: str, monitor_id: str) -> None:
        await self._client.request("DELETE", f"{_service_path(account_id, service_id)}/monitors/{monitor_id}")

    async def link_incidents(self, account_id: str, service_id: str, incident_ids: list[str]) -> None:
        await self._client.request(
            "POST",
            f"{_service_path(account_id, service_id)}/incidents",
            json={"incident_ids": incident_ids},
        )

    async def unlink_incident(self, account_id: str, service_id: str, incident_id: str) -> None:
        await self._client.request("DELETE", f"{_service_path(account_id, service_id)}/incidents/{incident_id}")

    async def get_analytics(self, account_id: str, service_id: str) -> ServiceAnalytics:
        resp = await self._client.request("GET", f"{_service_path(account_id, service_id)}/analytics")
        return ServiceAnalytics.model_validate_json(resp)


class Services:
    def __init__(self, client: BaseClient) -> None:
        self._client = client

    def create(self, account_id: str, params: CreateServiceParams) -> Service:
        resp = self._client.request("POST", _base_path(account_id), json=params.model_dump(exclude_none=True))
        return Service.model_validate_json(resp)

    def list(self, account_id: str) -> list[Service]:
        resp = self._client.request("GET", _base_path(account_id))
        return [Service.model_validate(s) for s in json.loads(resp)]

    def get(self, account_id: str, service_id: str) -> Service:
        resp = self._client.request("GET", _service_path(account_id, service_id))
        return Service.model_validate_json(resp)

    def update(self, account_id: str, service_id: str, params: UpdateServiceParams) -> Service:
        resp = self._client.request(
            "PUT", _service_path(account_id, service_id), json=params.model_dump(exclude_none=True)
        )
        return Service.model_validate_json(resp)

    def delete(self, account_id: str, service_id: str) -> None:
        self._client.request("DELETE", _service_path(account_id, service_id))

    def link_monitors(self, account_id: str, service_id: str, monitor_ids: list[str]) -> None:
        self._client.request(
            "POST",
            f"{_service_path(account_id, service_id)}/monitors",
            json={"monitor_ids": monitor_ids},
        )

    def unlink_monitor(self, account_id: str, service_id: str, monitor_id: str) -> None:
        self._client.request("DELETE", f"{_service_path(account_id, service_id)}/monitors/{monitor_id}")

    def link_incidents(self, account_id: str, service_id: str, incident_ids: list[str]) -> None:
        self._client.request(
            "POST",
            f"{_service_path(account_id, service_id)}/incidents",
            json={"incident_ids": incident_ids},
        )

    def unlink_incident(self, account_id: str, service_id: str, incident_id: str) -> None:
        self._client.request("DELETE", f"{_service_path(account_id, service_id)}/incidents/{incident_id}")

    def get_analytics(self, account_id: str, service_id: str) -> ServiceAnalytics:
        resp = self._client.request("GET", f"{_service_path(account_id, service_id)}/analytics")
        return ServiceAnalytics.model_validate_json(resp)
