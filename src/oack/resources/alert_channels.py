"""Alert channel resource."""

from __future__ import annotations

import json
from typing import TYPE_CHECKING

from oack.types.alert_channels import AlertChannel, AlertEvent, CreateAlertChannelParams

if TYPE_CHECKING:
    from oack._client import AsyncBaseClient, BaseClient


class AsyncAlertChannels:
    def __init__(self, client: AsyncBaseClient) -> None:
        self._client = client

    async def create(self, team_id: str, params: CreateAlertChannelParams) -> AlertChannel:
        resp = await self._client.request(
            "POST", f"/api/v1/teams/{team_id}/alert-channels", json=params.model_dump(exclude_none=True)
        )
        return AlertChannel.model_validate_json(resp)

    async def list(self, team_id: str) -> list[AlertChannel]:
        resp = await self._client.request("GET", f"/api/v1/teams/{team_id}/alert-channels")
        return [AlertChannel.model_validate(c) for c in json.loads(resp)]

    async def get(self, team_id: str, channel_id: str) -> AlertChannel:
        channels = await self.list(team_id)
        for ch in channels:
            if ch.id == channel_id:
                return ch
        from oack._exceptions import NotFoundError

        raise NotFoundError("alert channel not found")

    async def update(self, team_id: str, channel_id: str, params: CreateAlertChannelParams) -> AlertChannel:
        resp = await self._client.request(
            "PUT",
            f"/api/v1/teams/{team_id}/alert-channels/{channel_id}",
            json=params.model_dump(exclude_none=True),
        )
        return AlertChannel.model_validate_json(resp)

    async def delete(self, team_id: str, channel_id: str) -> None:
        await self._client.request("DELETE", f"/api/v1/teams/{team_id}/alert-channels/{channel_id}")

    async def test(self, team_id: str, channel_id: str) -> None:
        await self._client.request("POST", f"/api/v1/teams/{team_id}/alert-channels/{channel_id}/test")

    async def list_monitor_channels(self, team_id: str, monitor_id: str) -> list[str]:
        resp = await self._client.request("GET", f"/api/v1/teams/{team_id}/monitors/{monitor_id}/alert-channels")
        return json.loads(resp).get("channel_ids", [])

    async def set_monitor_channels(self, team_id: str, monitor_id: str, channel_ids: list[str]) -> list[str]:
        resp = await self._client.request(
            "PUT",
            f"/api/v1/teams/{team_id}/monitors/{monitor_id}/alert-channels",
            json={"channel_ids": channel_ids},
        )
        return json.loads(resp).get("channel_ids", [])

    async def link_monitor_channel(self, team_id: str, monitor_id: str, channel_id: str) -> None:
        await self._client.request("POST", f"/api/v1/teams/{team_id}/monitors/{monitor_id}/alert-channels/{channel_id}")

    async def unlink_monitor_channel(self, team_id: str, monitor_id: str, channel_id: str) -> None:
        await self._client.request(
            "DELETE", f"/api/v1/teams/{team_id}/monitors/{monitor_id}/alert-channels/{channel_id}"
        )

    async def list_events(self, team_id: str, monitor_id: str) -> list[AlertEvent]:
        resp = await self._client.request("GET", f"/api/v1/teams/{team_id}/monitors/{monitor_id}/alert-events")
        return [AlertEvent.model_validate(e) for e in json.loads(resp)]


class AlertChannels:
    def __init__(self, client: BaseClient) -> None:
        self._client = client

    def create(self, team_id: str, params: CreateAlertChannelParams) -> AlertChannel:
        resp = self._client.request(
            "POST", f"/api/v1/teams/{team_id}/alert-channels", json=params.model_dump(exclude_none=True)
        )
        return AlertChannel.model_validate_json(resp)

    def list(self, team_id: str) -> list[AlertChannel]:
        resp = self._client.request("GET", f"/api/v1/teams/{team_id}/alert-channels")
        return [AlertChannel.model_validate(c) for c in json.loads(resp)]

    def get(self, team_id: str, channel_id: str) -> AlertChannel:
        channels = self.list(team_id)
        for ch in channels:
            if ch.id == channel_id:
                return ch
        from oack._exceptions import NotFoundError

        raise NotFoundError("alert channel not found")

    def update(self, team_id: str, channel_id: str, params: CreateAlertChannelParams) -> AlertChannel:
        resp = self._client.request(
            "PUT",
            f"/api/v1/teams/{team_id}/alert-channels/{channel_id}",
            json=params.model_dump(exclude_none=True),
        )
        return AlertChannel.model_validate_json(resp)

    def delete(self, team_id: str, channel_id: str) -> None:
        self._client.request("DELETE", f"/api/v1/teams/{team_id}/alert-channels/{channel_id}")

    def test(self, team_id: str, channel_id: str) -> None:
        self._client.request("POST", f"/api/v1/teams/{team_id}/alert-channels/{channel_id}/test")

    def list_monitor_channels(self, team_id: str, monitor_id: str) -> list[str]:
        resp = self._client.request("GET", f"/api/v1/teams/{team_id}/monitors/{monitor_id}/alert-channels")
        return json.loads(resp).get("channel_ids", [])

    def set_monitor_channels(self, team_id: str, monitor_id: str, channel_ids: list[str]) -> list[str]:
        resp = self._client.request(
            "PUT",
            f"/api/v1/teams/{team_id}/monitors/{monitor_id}/alert-channels",
            json={"channel_ids": channel_ids},
        )
        return json.loads(resp).get("channel_ids", [])

    def link_monitor_channel(self, team_id: str, monitor_id: str, channel_id: str) -> None:
        self._client.request("POST", f"/api/v1/teams/{team_id}/monitors/{monitor_id}/alert-channels/{channel_id}")

    def unlink_monitor_channel(self, team_id: str, monitor_id: str, channel_id: str) -> None:
        self._client.request("DELETE", f"/api/v1/teams/{team_id}/monitors/{monitor_id}/alert-channels/{channel_id}")

    def list_events(self, team_id: str, monitor_id: str) -> list[AlertEvent]:
        resp = self._client.request("GET", f"/api/v1/teams/{team_id}/monitors/{monitor_id}/alert-events")
        return [AlertEvent.model_validate(e) for e in json.loads(resp)]
