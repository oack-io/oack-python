"""Share resource."""

from __future__ import annotations

import json
from typing import TYPE_CHECKING

from oack.types.shares import CreateShareParams, Share

if TYPE_CHECKING:
    from oack._client import AsyncBaseClient, BaseClient


def _shares_path(team_id: str, monitor_id: str) -> str:
    return f"/api/v1/teams/{team_id}/monitors/{monitor_id}/shares"


class AsyncShares:
    def __init__(self, client: AsyncBaseClient) -> None:
        self._client = client

    async def create(self, team_id: str, monitor_id: str, params: CreateShareParams) -> Share:
        resp = await self._client.request("POST", _shares_path(team_id, monitor_id), json=params.to_request_body())
        return Share.model_validate_json(resp)

    async def list(self, team_id: str, monitor_id: str) -> list[Share]:
        resp = await self._client.request("GET", _shares_path(team_id, monitor_id))
        return [Share.model_validate(s) for s in json.loads(resp)]

    async def revoke(self, team_id: str, monitor_id: str, share_id: str) -> None:
        await self._client.request("DELETE", _shares_path(team_id, monitor_id) + f"/{share_id}")


class Shares:
    def __init__(self, client: BaseClient) -> None:
        self._client = client

    def create(self, team_id: str, monitor_id: str, params: CreateShareParams) -> Share:
        resp = self._client.request("POST", _shares_path(team_id, monitor_id), json=params.to_request_body())
        return Share.model_validate_json(resp)

    def list(self, team_id: str, monitor_id: str) -> list[Share]:
        resp = self._client.request("GET", _shares_path(team_id, monitor_id))
        return [Share.model_validate(s) for s in json.loads(resp)]

    def revoke(self, team_id: str, monitor_id: str, share_id: str) -> None:
        self._client.request("DELETE", _shares_path(team_id, monitor_id) + f"/{share_id}")
