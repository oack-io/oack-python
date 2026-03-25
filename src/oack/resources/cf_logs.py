"""Cloudflare log resource."""

from __future__ import annotations

import json
from typing import TYPE_CHECKING, Any

from oack.types.cf_logs import CFLogEntry

if TYPE_CHECKING:
    from oack._client import AsyncBaseClient, BaseClient


def _monitor_path(team_id: str, monitor_id: str) -> str:
    return f"/api/v1/teams/{team_id}/monitors/{monitor_id}"


class AsyncCFLogs:
    def __init__(self, client: AsyncBaseClient) -> None:
        self._client = client

    async def get(self, team_id: str, monitor_id: str, probe_id: str) -> CFLogEntry:
        resp = await self._client.request(
            "GET", _monitor_path(team_id, monitor_id) + f"/probes/{probe_id}/cf-log"
        )
        return CFLogEntry.model_validate_json(resp)

    async def list(
        self,
        team_id: str,
        monitor_id: str,
        from_ts: str | None = None,
        to_ts: str | None = None,
        limit: int | None = None,
    ) -> list[CFLogEntry]:
        params: dict[str, Any] = {}
        if from_ts is not None:
            params["from"] = from_ts
        if to_ts is not None:
            params["to"] = to_ts
        if limit is not None:
            params["limit"] = limit
        resp = await self._client.request(
            "GET", _monitor_path(team_id, monitor_id) + "/cf-logs", params=params
        )
        return [CFLogEntry.model_validate(e) for e in json.loads(resp)]


class CFLogs:
    def __init__(self, client: BaseClient) -> None:
        self._client = client

    def get(self, team_id: str, monitor_id: str, probe_id: str) -> CFLogEntry:
        resp = self._client.request(
            "GET", _monitor_path(team_id, monitor_id) + f"/probes/{probe_id}/cf-log"
        )
        return CFLogEntry.model_validate_json(resp)

    def list(
        self,
        team_id: str,
        monitor_id: str,
        from_ts: str | None = None,
        to_ts: str | None = None,
        limit: int | None = None,
    ) -> list[CFLogEntry]:
        params: dict[str, Any] = {}
        if from_ts is not None:
            params["from"] = from_ts
        if to_ts is not None:
            params["to"] = to_ts
        if limit is not None:
            params["limit"] = limit
        resp = self._client.request(
            "GET", _monitor_path(team_id, monitor_id) + "/cf-logs", params=params
        )
        return [CFLogEntry.model_validate(e) for e in json.loads(resp)]
