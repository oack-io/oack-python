"""Trace resource."""

from __future__ import annotations

import json
from typing import TYPE_CHECKING

from oack.types.traces import Trace

if TYPE_CHECKING:
    from oack._client import AsyncBaseClient, BaseClient


def _traces_path(team_id: str, monitor_id: str) -> str:
    return f"/api/v1/teams/{team_id}/monitors/{monitor_id}/traces"


class AsyncTraces:
    def __init__(self, client: AsyncBaseClient) -> None:
        self._client = client

    async def list(self, team_id: str, monitor_id: str) -> list[Trace]:
        resp = await self._client.request("GET", _traces_path(team_id, monitor_id))
        return [Trace.model_validate(t) for t in json.loads(resp)]

    async def request(self, team_id: str, monitor_id: str) -> Trace:
        resp = await self._client.request("POST", _traces_path(team_id, monitor_id))
        return Trace.model_validate_json(resp)


class Traces:
    def __init__(self, client: BaseClient) -> None:
        self._client = client

    def list(self, team_id: str, monitor_id: str) -> list[Trace]:
        resp = self._client.request("GET", _traces_path(team_id, monitor_id))
        return [Trace.model_validate(t) for t in json.loads(resp)]

    def request(self, team_id: str, monitor_id: str) -> Trace:
        resp = self._client.request("POST", _traces_path(team_id, monitor_id))
        return Trace.model_validate_json(resp)
