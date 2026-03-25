"""Notification resource."""

from __future__ import annotations

from typing import TYPE_CHECKING

from oack.types.notifications import MonitorNotification, NotificationDefaults

if TYPE_CHECKING:
    from oack._client import AsyncBaseClient, BaseClient


class AsyncNotifications:
    def __init__(self, client: AsyncBaseClient) -> None:
        self._client = client

    async def get_defaults(self, account_id: str) -> NotificationDefaults:
        resp = await self._client.request("GET", f"/api/v1/me/accounts/{account_id}/notification-defaults")
        return NotificationDefaults.model_validate_json(resp)

    async def set_defaults(self, account_id: str, channel_ids: list[str]) -> NotificationDefaults:
        resp = await self._client.request(
            "PUT",
            f"/api/v1/me/accounts/{account_id}/notification-defaults",
            json={"channel_ids": channel_ids},
        )
        return NotificationDefaults.model_validate_json(resp)

    async def copy_channels(self, from_account_id: str, to_account_id: str) -> None:
        await self._client.request(
            "POST",
            "/api/v1/me/alert-channels/copy",
            json={"from_account_id": from_account_id, "to_account_id": to_account_id},
        )

    async def get_monitor(self, team_id: str, monitor_id: str) -> MonitorNotification:
        resp = await self._client.request("GET", f"/api/v1/teams/{team_id}/monitors/{monitor_id}/my/notifications")
        return MonitorNotification.model_validate_json(resp)

    async def set_monitor(self, team_id: str, monitor_id: str, channel_ids: list[str]) -> MonitorNotification:
        resp = await self._client.request(
            "PUT",
            f"/api/v1/teams/{team_id}/monitors/{monitor_id}/my/notifications",
            json={"channel_ids": channel_ids},
        )
        return MonitorNotification.model_validate_json(resp)

    async def remove_monitor(self, team_id: str, monitor_id: str) -> None:
        await self._client.request("DELETE", f"/api/v1/teams/{team_id}/monitors/{monitor_id}/my/notifications")


class Notifications:
    def __init__(self, client: BaseClient) -> None:
        self._client = client

    def get_defaults(self, account_id: str) -> NotificationDefaults:
        resp = self._client.request("GET", f"/api/v1/me/accounts/{account_id}/notification-defaults")
        return NotificationDefaults.model_validate_json(resp)

    def set_defaults(self, account_id: str, channel_ids: list[str]) -> NotificationDefaults:
        resp = self._client.request(
            "PUT",
            f"/api/v1/me/accounts/{account_id}/notification-defaults",
            json={"channel_ids": channel_ids},
        )
        return NotificationDefaults.model_validate_json(resp)

    def copy_channels(self, from_account_id: str, to_account_id: str) -> None:
        self._client.request(
            "POST",
            "/api/v1/me/alert-channels/copy",
            json={"from_account_id": from_account_id, "to_account_id": to_account_id},
        )

    def get_monitor(self, team_id: str, monitor_id: str) -> MonitorNotification:
        resp = self._client.request("GET", f"/api/v1/teams/{team_id}/monitors/{monitor_id}/my/notifications")
        return MonitorNotification.model_validate_json(resp)

    def set_monitor(self, team_id: str, monitor_id: str, channel_ids: list[str]) -> MonitorNotification:
        resp = self._client.request(
            "PUT",
            f"/api/v1/teams/{team_id}/monitors/{monitor_id}/my/notifications",
            json={"channel_ids": channel_ids},
        )
        return MonitorNotification.model_validate_json(resp)

    def remove_monitor(self, team_id: str, monitor_id: str) -> None:
        self._client.request("DELETE", f"/api/v1/teams/{team_id}/monitors/{monitor_id}/my/notifications")
