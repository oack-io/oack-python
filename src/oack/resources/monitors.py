"""Monitor resource."""

from __future__ import annotations

import json
from typing import TYPE_CHECKING, Any

from oack.types.monitors import CreateMonitorParams, Monitor

if TYPE_CHECKING:
    from oack._client import AsyncBaseClient, BaseClient


def _monitor_path(team_id: str, monitor_id: str) -> str:
    return f"/api/v1/teams/{team_id}/monitors/{monitor_id}"


class AsyncMonitors:
    def __init__(self, client: AsyncBaseClient) -> None:
        self._client = client

    async def create(self, team_id: str, params: CreateMonitorParams) -> Monitor:
        resp = await self._client.request(
            "POST", f"/api/v1/teams/{team_id}/monitors", json=params.to_request_body()
        )
        return Monitor.model_validate_json(resp)

    async def list(self, team_id: str) -> list[Monitor]:
        resp = await self._client.request("GET", f"/api/v1/teams/{team_id}/monitors")
        return [Monitor.model_validate(m) for m in json.loads(resp)]

    async def get(self, team_id: str, monitor_id: str) -> Monitor:
        resp = await self._client.request("GET", _monitor_path(team_id, monitor_id))
        return Monitor.model_validate_json(resp)

    async def update(self, team_id: str, monitor_id: str, params: CreateMonitorParams) -> Monitor:
        resp = await self._client.request(
            "PUT", _monitor_path(team_id, monitor_id), json=params.to_request_body()
        )
        return Monitor.model_validate_json(resp)

    async def delete(self, team_id: str, monitor_id: str) -> None:
        await self._client.request("DELETE", _monitor_path(team_id, monitor_id))

    async def pause(self, team_id: str, monitor_id: str) -> Monitor:
        resp = await self._client.request("POST", _monitor_path(team_id, monitor_id) + "/pause")
        return Monitor.model_validate_json(resp)

    async def unpause(self, team_id: str, monitor_id: str) -> Monitor:
        resp = await self._client.request("POST", _monitor_path(team_id, monitor_id) + "/unpause")
        return Monitor.model_validate_json(resp)

    async def duplicate(self, team_id: str, monitor_id: str) -> Monitor:
        resp = await self._client.request("POST", _monitor_path(team_id, monitor_id) + "/duplicate")
        return Monitor.model_validate_json(resp)

    async def move(self, team_id: str, monitor_id: str, target_team_id: str) -> Monitor:
        resp = await self._client.request(
            "POST", _monitor_path(team_id, monitor_id) + "/move", json={"target_team_id": target_team_id}
        )
        return Monitor.model_validate_json(resp)

    async def test_alert(self, team_id: str, monitor_id: str) -> None:
        await self._client.request("POST", _monitor_path(team_id, monitor_id) + "/test-alert")


class Monitors:
    def __init__(self, client: BaseClient) -> None:
        self._client = client

    def create(self, team_id: str, params: CreateMonitorParams) -> Monitor:
        resp = self._client.request("POST", f"/api/v1/teams/{team_id}/monitors", json=params.to_request_body())
        return Monitor.model_validate_json(resp)

    def list(self, team_id: str) -> list[Monitor]:
        resp = self._client.request("GET", f"/api/v1/teams/{team_id}/monitors")
        return [Monitor.model_validate(m) for m in json.loads(resp)]

    def get(self, team_id: str, monitor_id: str) -> Monitor:
        resp = self._client.request("GET", _monitor_path(team_id, monitor_id))
        return Monitor.model_validate_json(resp)

    def update(self, team_id: str, monitor_id: str, params: CreateMonitorParams) -> Monitor:
        resp = self._client.request("PUT", _monitor_path(team_id, monitor_id), json=params.to_request_body())
        return Monitor.model_validate_json(resp)

    def delete(self, team_id: str, monitor_id: str) -> None:
        self._client.request("DELETE", _monitor_path(team_id, monitor_id))

    def pause(self, team_id: str, monitor_id: str) -> Monitor:
        resp = self._client.request("POST", _monitor_path(team_id, monitor_id) + "/pause")
        return Monitor.model_validate_json(resp)

    def unpause(self, team_id: str, monitor_id: str) -> Monitor:
        resp = self._client.request("POST", _monitor_path(team_id, monitor_id) + "/unpause")
        return Monitor.model_validate_json(resp)

    def duplicate(self, team_id: str, monitor_id: str) -> Monitor:
        resp = self._client.request("POST", _monitor_path(team_id, monitor_id) + "/duplicate")
        return Monitor.model_validate_json(resp)

    def move(self, team_id: str, monitor_id: str, target_team_id: str) -> Monitor:
        resp = self._client.request(
            "POST", _monitor_path(team_id, monitor_id) + "/move", json={"target_team_id": target_team_id}
        )
        return Monitor.model_validate_json(resp)

    def test_alert(self, team_id: str, monitor_id: str) -> None:
        self._client.request("POST", _monitor_path(team_id, monitor_id) + "/test-alert")
