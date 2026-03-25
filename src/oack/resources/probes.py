"""Probe resource."""

from __future__ import annotations

import json
from typing import TYPE_CHECKING, Any

from oack.types.probes import Probe, ProbeAggregation, ProbeList

if TYPE_CHECKING:
    from oack._client import AsyncBaseClient, BaseClient


def _probe_path(team_id: str, monitor_id: str) -> str:
    return f"/api/v1/teams/{team_id}/monitors/{monitor_id}/probes"


def _build_list_params(
    limit: int | None = None,
    offset: int | None = None,
    is_up: bool | None = None,
) -> dict[str, str]:
    params: dict[str, str] = {}
    if limit is not None:
        params["limit"] = str(limit)
    if offset is not None:
        params["offset"] = str(offset)
    if is_up is not None:
        params["is_up"] = str(is_up).lower()
    return params


class AsyncProbes:
    def __init__(self, client: AsyncBaseClient) -> None:
        self._client = client

    async def list(
        self,
        team_id: str,
        monitor_id: str,
        *,
        limit: int | None = None,
        offset: int | None = None,
        is_up: bool | None = None,
    ) -> ProbeList:
        params = _build_list_params(limit, offset, is_up)
        resp = await self._client.request("GET", _probe_path(team_id, monitor_id), params=params or None)
        return ProbeList.model_validate_json(resp)

    async def get(self, team_id: str, monitor_id: str, probe_id: str) -> Probe:
        resp = await self._client.request("GET", f"{_probe_path(team_id, monitor_id)}/{probe_id}")
        return Probe.model_validate_json(resp)

    async def get_details(self, team_id: str, monitor_id: str, probe_id: str) -> dict[str, Any]:
        resp = await self._client.request("GET", f"{_probe_path(team_id, monitor_id)}/{probe_id}/details")
        return json.loads(resp)  # type: ignore[no-any-return]

    async def download_pcap(self, team_id: str, monitor_id: str, probe_id: str) -> bytes:
        return await self._client.request("GET", f"{_probe_path(team_id, monitor_id)}/{probe_id}/pcap")

    async def aggregate(
        self,
        team_id: str,
        monitor_id: str,
        *,
        from_ts: int,
        to_ts: int,
        step: str,
        agg: str,
    ) -> ProbeAggregation:
        params = {"from": str(from_ts), "to": str(to_ts), "step": step, "agg": agg}
        resp = await self._client.request("GET", f"{_probe_path(team_id, monitor_id)}/aggregate", params=params)
        return ProbeAggregation.model_validate_json(resp)


class Probes:
    def __init__(self, client: BaseClient) -> None:
        self._client = client

    def list(
        self,
        team_id: str,
        monitor_id: str,
        *,
        limit: int | None = None,
        offset: int | None = None,
        is_up: bool | None = None,
    ) -> ProbeList:
        params = _build_list_params(limit, offset, is_up)
        resp = self._client.request("GET", _probe_path(team_id, monitor_id), params=params or None)
        return ProbeList.model_validate_json(resp)

    def get(self, team_id: str, monitor_id: str, probe_id: str) -> Probe:
        resp = self._client.request("GET", f"{_probe_path(team_id, monitor_id)}/{probe_id}")
        return Probe.model_validate_json(resp)

    def get_details(self, team_id: str, monitor_id: str, probe_id: str) -> dict[str, Any]:
        resp = self._client.request("GET", f"{_probe_path(team_id, monitor_id)}/{probe_id}/details")
        return json.loads(resp)  # type: ignore[no-any-return]

    def download_pcap(self, team_id: str, monitor_id: str, probe_id: str) -> bytes:
        return self._client.request("GET", f"{_probe_path(team_id, monitor_id)}/{probe_id}/pcap")

    def aggregate(
        self,
        team_id: str,
        monitor_id: str,
        *,
        from_ts: int,
        to_ts: int,
        step: str,
        agg: str,
    ) -> ProbeAggregation:
        params = {"from": str(from_ts), "to": str(to_ts), "step": step, "agg": agg}
        resp = self._client.request("GET", f"{_probe_path(team_id, monitor_id)}/aggregate", params=params)
        return ProbeAggregation.model_validate_json(resp)
