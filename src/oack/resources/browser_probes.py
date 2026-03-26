"""Browser probe resource."""

from __future__ import annotations

from typing import TYPE_CHECKING

from oack.types.browser_probes import BrowserProbe, BrowserProbeAggregation, BrowserProbeList

if TYPE_CHECKING:
    from oack._client import AsyncBaseClient, BaseClient


def _browser_probe_path(team_id: str, monitor_id: str) -> str:
    return f"/api/v1/teams/{team_id}/monitors/{monitor_id}/browser-probes"


class AsyncBrowserProbes:
    def __init__(self, client: AsyncBaseClient) -> None:
        self._client = client

    async def list(
        self,
        team_id: str,
        monitor_id: str,
        *,
        from_ts: str | None = None,
        to_ts: str | None = None,
        limit: int | None = None,
    ) -> BrowserProbeList:
        params: dict[str, str] = {}
        if from_ts is not None:
            params["from"] = from_ts
        if to_ts is not None:
            params["to"] = to_ts
        if limit is not None:
            params["limit"] = str(limit)
        resp = await self._client.request("GET", _browser_probe_path(team_id, monitor_id), params=params or None)
        return BrowserProbeList.model_validate_json(resp)

    async def get(self, team_id: str, monitor_id: str, probe_id: str) -> BrowserProbe:
        resp = await self._client.request("GET", f"{_browser_probe_path(team_id, monitor_id)}/{probe_id}")
        return BrowserProbe.model_validate_json(resp)

    async def aggregate(
        self,
        team_id: str,
        monitor_id: str,
        *,
        from_ts: str,
        to_ts: str,
        step: str | None = None,
    ) -> BrowserProbeAggregation:
        params: dict[str, str] = {"from": from_ts, "to": to_ts}
        if step is not None:
            params["step"] = step
        resp = await self._client.request("GET", f"{_browser_probe_path(team_id, monitor_id)}/aggregate", params=params)
        return BrowserProbeAggregation.model_validate_json(resp)

    async def download_screenshot(self, team_id: str, monitor_id: str, probe_id: str) -> bytes:
        return await self._client.request("GET", f"{_browser_probe_path(team_id, monitor_id)}/{probe_id}/screenshot")

    async def download_har(self, team_id: str, monitor_id: str, probe_id: str) -> bytes:
        return await self._client.request("GET", f"{_browser_probe_path(team_id, monitor_id)}/{probe_id}/har")


class BrowserProbes:
    def __init__(self, client: BaseClient) -> None:
        self._client = client

    def list(
        self,
        team_id: str,
        monitor_id: str,
        *,
        from_ts: str | None = None,
        to_ts: str | None = None,
        limit: int | None = None,
    ) -> BrowserProbeList:
        params: dict[str, str] = {}
        if from_ts is not None:
            params["from"] = from_ts
        if to_ts is not None:
            params["to"] = to_ts
        if limit is not None:
            params["limit"] = str(limit)
        resp = self._client.request("GET", _browser_probe_path(team_id, monitor_id), params=params or None)
        return BrowserProbeList.model_validate_json(resp)

    def get(self, team_id: str, monitor_id: str, probe_id: str) -> BrowserProbe:
        resp = self._client.request("GET", f"{_browser_probe_path(team_id, monitor_id)}/{probe_id}")
        return BrowserProbe.model_validate_json(resp)

    def aggregate(
        self,
        team_id: str,
        monitor_id: str,
        *,
        from_ts: str,
        to_ts: str,
        step: str | None = None,
    ) -> BrowserProbeAggregation:
        params: dict[str, str] = {"from": from_ts, "to": to_ts}
        if step is not None:
            params["step"] = step
        resp = self._client.request("GET", f"{_browser_probe_path(team_id, monitor_id)}/aggregate", params=params)
        return BrowserProbeAggregation.model_validate_json(resp)

    def download_screenshot(self, team_id: str, monitor_id: str, probe_id: str) -> bytes:
        return self._client.request("GET", f"{_browser_probe_path(team_id, monitor_id)}/{probe_id}/screenshot")

    def download_har(self, team_id: str, monitor_id: str, probe_id: str) -> bytes:
        return self._client.request("GET", f"{_browser_probe_path(team_id, monitor_id)}/{probe_id}/har")
