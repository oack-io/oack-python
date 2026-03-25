"""User resource."""

from __future__ import annotations

import json
from typing import TYPE_CHECKING

from oack.types.user import Device, Preferences, TelegramLink, TelegramLinkStatus, User

if TYPE_CHECKING:
    from oack._client import AsyncBaseClient, BaseClient


class AsyncUser:
    def __init__(self, client: AsyncBaseClient) -> None:
        self._client = client

    async def whoami(self) -> User:
        resp = await self._client.request("GET", "/api/v1/me")
        return User.model_validate_json(resp)

    async def get_preferences(self) -> Preferences:
        resp = await self._client.request("GET", "/api/v1/me/preferences")
        return Preferences.model_validate_json(resp)

    async def update_preferences(self, params: dict) -> Preferences:
        resp = await self._client.request("PUT", "/api/v1/me/preferences", json=params)
        return Preferences.model_validate_json(resp)

    async def register_device(self, token: str, platform: str) -> Device:
        resp = await self._client.request("POST", "/api/v1/me/devices", json={"token": token, "platform": platform})
        return Device.model_validate_json(resp)

    async def list_devices(self) -> list[Device]:
        resp = await self._client.request("GET", "/api/v1/me/devices")
        return [Device.model_validate(d) for d in json.loads(resp)]

    async def unregister_device(self, token: str) -> None:
        await self._client.request("DELETE", f"/api/v1/me/devices/{token}")

    async def create_telegram_link(self) -> TelegramLink:
        resp = await self._client.request("POST", "/api/v1/me/telegram-link")
        return TelegramLink.model_validate_json(resp)

    async def get_telegram_link_status(self, code: str) -> TelegramLinkStatus:
        resp = await self._client.request("GET", f"/api/v1/me/telegram-link/{code}/status")
        return TelegramLinkStatus.model_validate_json(resp)


class SyncUser:
    """Sync user resource."""

    def __init__(self, client: BaseClient) -> None:
        self._client = client

    def whoami(self) -> User:
        resp = self._client.request("GET", "/api/v1/me")
        return User.model_validate_json(resp)

    def get_preferences(self) -> Preferences:
        resp = self._client.request("GET", "/api/v1/me/preferences")
        return Preferences.model_validate_json(resp)

    def update_preferences(self, params: dict) -> Preferences:
        resp = self._client.request("PUT", "/api/v1/me/preferences", json=params)
        return Preferences.model_validate_json(resp)

    def register_device(self, token: str, platform: str) -> Device:
        resp = self._client.request("POST", "/api/v1/me/devices", json={"token": token, "platform": platform})
        return Device.model_validate_json(resp)

    def list_devices(self) -> list[Device]:
        resp = self._client.request("GET", "/api/v1/me/devices")
        return [Device.model_validate(d) for d in json.loads(resp)]

    def unregister_device(self, token: str) -> None:
        self._client.request("DELETE", f"/api/v1/me/devices/{token}")

    def create_telegram_link(self) -> TelegramLink:
        resp = self._client.request("POST", "/api/v1/me/telegram-link")
        return TelegramLink.model_validate_json(resp)

    def get_telegram_link_status(self, code: str) -> TelegramLinkStatus:
        resp = self._client.request("GET", f"/api/v1/me/telegram-link/{code}/status")
        return TelegramLinkStatus.model_validate_json(resp)
