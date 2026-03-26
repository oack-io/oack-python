"""Metrics, timeline, and chart events resource."""

from __future__ import annotations

import json
from typing import TYPE_CHECKING

from oack.types.metrics import (
    ChartEvent,
    CreateChartEventParams,
    Expiration,
    IngestChartEventParams,
    MonitorMetrics,
    TimelineEvent,
    UpdateChartEventParams,
)

if TYPE_CHECKING:
    from oack._client import AsyncBaseClient, BaseClient


class AsyncMetrics:
    def __init__(self, client: AsyncBaseClient) -> None:
        self._client = client

    async def get_monitor_metrics(self, team_id: str, monitor_id: str) -> MonitorMetrics:
        resp = await self._client.request("GET", f"/api/v1/teams/{team_id}/monitors/{monitor_id}/metrics")
        return MonitorMetrics.model_validate_json(resp)

    async def get_expiration(self, team_id: str, monitor_id: str) -> Expiration:
        resp = await self._client.request("GET", f"/api/v1/teams/{team_id}/monitors/{monitor_id}/expiration")
        return Expiration.model_validate_json(resp)

    async def list_timeline(
        self,
        team_id: str,
        monitor_id: str,
        *,
        limit: int | None = None,
        offset: int | None = None,
    ) -> list[TimelineEvent]:
        params: dict[str, str] = {}
        if limit is not None:
            params["limit"] = str(limit)
        if offset is not None:
            params["offset"] = str(offset)
        resp = await self._client.request(
            "GET", f"/api/v1/teams/{team_id}/monitors/{monitor_id}/timeline", params=params or None
        )
        return [TimelineEvent.model_validate(e) for e in json.loads(resp)]

    async def create_chart_event(self, team_id: str, params: CreateChartEventParams) -> ChartEvent:
        resp = await self._client.request(
            "POST", f"/api/v1/teams/{team_id}/events", json=params.model_dump(exclude_none=True)
        )
        return ChartEvent.model_validate_json(resp)

    async def list_chart_events(
        self,
        team_id: str,
        *,
        from_ts: str,
        to_ts: str,
        monitor_id: str | None = None,
        kind: str | None = None,
        source: str | None = None,
    ) -> list[ChartEvent]:
        params: dict[str, str] = {"from": from_ts, "to": to_ts}
        if monitor_id is not None:
            params["monitor_id"] = monitor_id
        if kind is not None:
            params["kind"] = kind
        if source is not None:
            params["source"] = source
        resp = await self._client.request("GET", f"/api/v1/teams/{team_id}/events", params=params)
        return [ChartEvent.model_validate(e) for e in json.loads(resp)]

    async def update_chart_event(self, team_id: str, event_id: str, params: UpdateChartEventParams) -> ChartEvent:
        resp = await self._client.request(
            "PUT", f"/api/v1/teams/{team_id}/events/{event_id}", json=params.model_dump(exclude_none=True)
        )
        return ChartEvent.model_validate_json(resp)

    async def delete_chart_event(self, team_id: str, event_id: str) -> None:
        await self._client.request("DELETE", f"/api/v1/teams/{team_id}/events/{event_id}")

    async def ingest_chart_event(self, team_id: str, params: IngestChartEventParams) -> ChartEvent:
        resp = await self._client.request(
            "POST", f"/api/v1/teams/{team_id}/events/ingest", json=params.model_dump(exclude_none=True)
        )
        return ChartEvent.model_validate_json(resp)


class Metrics:
    def __init__(self, client: BaseClient) -> None:
        self._client = client

    def get_monitor_metrics(self, team_id: str, monitor_id: str) -> MonitorMetrics:
        resp = self._client.request("GET", f"/api/v1/teams/{team_id}/monitors/{monitor_id}/metrics")
        return MonitorMetrics.model_validate_json(resp)

    def get_expiration(self, team_id: str, monitor_id: str) -> Expiration:
        resp = self._client.request("GET", f"/api/v1/teams/{team_id}/monitors/{monitor_id}/expiration")
        return Expiration.model_validate_json(resp)

    def list_timeline(
        self,
        team_id: str,
        monitor_id: str,
        *,
        limit: int | None = None,
        offset: int | None = None,
    ) -> list[TimelineEvent]:
        params: dict[str, str] = {}
        if limit is not None:
            params["limit"] = str(limit)
        if offset is not None:
            params["offset"] = str(offset)
        resp = self._client.request(
            "GET", f"/api/v1/teams/{team_id}/monitors/{monitor_id}/timeline", params=params or None
        )
        return [TimelineEvent.model_validate(e) for e in json.loads(resp)]

    def create_chart_event(self, team_id: str, params: CreateChartEventParams) -> ChartEvent:
        resp = self._client.request(
            "POST", f"/api/v1/teams/{team_id}/events", json=params.model_dump(exclude_none=True)
        )
        return ChartEvent.model_validate_json(resp)

    def list_chart_events(
        self,
        team_id: str,
        *,
        from_ts: str,
        to_ts: str,
        monitor_id: str | None = None,
        kind: str | None = None,
        source: str | None = None,
    ) -> list[ChartEvent]:
        params: dict[str, str] = {"from": from_ts, "to": to_ts}
        if monitor_id is not None:
            params["monitor_id"] = monitor_id
        if kind is not None:
            params["kind"] = kind
        if source is not None:
            params["source"] = source
        resp = self._client.request("GET", f"/api/v1/teams/{team_id}/events", params=params)
        return [ChartEvent.model_validate(e) for e in json.loads(resp)]

    def update_chart_event(self, team_id: str, event_id: str, params: UpdateChartEventParams) -> ChartEvent:
        resp = self._client.request(
            "PUT", f"/api/v1/teams/{team_id}/events/{event_id}", json=params.model_dump(exclude_none=True)
        )
        return ChartEvent.model_validate_json(resp)

    def delete_chart_event(self, team_id: str, event_id: str) -> None:
        self._client.request("DELETE", f"/api/v1/teams/{team_id}/events/{event_id}")

    def ingest_chart_event(self, team_id: str, params: IngestChartEventParams) -> ChartEvent:
        resp = self._client.request(
            "POST", f"/api/v1/teams/{team_id}/events/ingest", json=params.model_dump(exclude_none=True)
        )
        return ChartEvent.model_validate_json(resp)
