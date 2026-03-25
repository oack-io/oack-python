"""External link resource."""

from __future__ import annotations

import json
from typing import TYPE_CHECKING

from oack.types.external_links import ExternalLink

if TYPE_CHECKING:
    from oack._client import AsyncBaseClient, BaseClient


class AsyncExternalLinks:
    def __init__(self, client: AsyncBaseClient) -> None:
        self._client = client

    async def create(self, team_id: str, params: dict) -> ExternalLink:
        resp = await self._client.request("POST", f"/api/v1/teams/{team_id}/external-links", json=params)
        return ExternalLink.model_validate_json(resp)

    async def list(self, team_id: str) -> list[ExternalLink]:
        resp = await self._client.request("GET", f"/api/v1/teams/{team_id}/external-links")
        return [ExternalLink.model_validate(lnk) for lnk in json.loads(resp)]

    async def get(self, team_id: str, link_id: str) -> ExternalLink:
        resp = await self._client.request("GET", f"/api/v1/teams/{team_id}/external-links/{link_id}")
        return ExternalLink.model_validate_json(resp)

    async def update(self, team_id: str, link_id: str, params: dict) -> ExternalLink:
        resp = await self._client.request("PUT", f"/api/v1/teams/{team_id}/external-links/{link_id}", json=params)
        return ExternalLink.model_validate_json(resp)

    async def delete(self, team_id: str, link_id: str) -> None:
        await self._client.request("DELETE", f"/api/v1/teams/{team_id}/external-links/{link_id}")

    async def assign(self, team_id: str, monitor_id: str, link_id: str) -> None:
        await self._client.request(
            "POST",
            f"/api/v1/teams/{team_id}/monitors/{monitor_id}/external-links/{link_id}",
        )

    async def unassign(self, team_id: str, monitor_id: str, link_id: str) -> None:
        await self._client.request(
            "DELETE",
            f"/api/v1/teams/{team_id}/monitors/{monitor_id}/external-links/{link_id}",
        )

    async def list_monitor_links(self, team_id: str, monitor_id: str) -> list[ExternalLink]:
        resp = await self._client.request("GET", f"/api/v1/teams/{team_id}/monitors/{monitor_id}/external-links")
        return [ExternalLink.model_validate(lnk) for lnk in json.loads(resp)]


class ExternalLinks:
    def __init__(self, client: BaseClient) -> None:
        self._client = client

    def create(self, team_id: str, params: dict) -> ExternalLink:
        resp = self._client.request("POST", f"/api/v1/teams/{team_id}/external-links", json=params)
        return ExternalLink.model_validate_json(resp)

    def list(self, team_id: str) -> list[ExternalLink]:
        resp = self._client.request("GET", f"/api/v1/teams/{team_id}/external-links")
        return [ExternalLink.model_validate(lnk) for lnk in json.loads(resp)]

    def get(self, team_id: str, link_id: str) -> ExternalLink:
        resp = self._client.request("GET", f"/api/v1/teams/{team_id}/external-links/{link_id}")
        return ExternalLink.model_validate_json(resp)

    def update(self, team_id: str, link_id: str, params: dict) -> ExternalLink:
        resp = self._client.request("PUT", f"/api/v1/teams/{team_id}/external-links/{link_id}", json=params)
        return ExternalLink.model_validate_json(resp)

    def delete(self, team_id: str, link_id: str) -> None:
        self._client.request("DELETE", f"/api/v1/teams/{team_id}/external-links/{link_id}")

    def assign(self, team_id: str, monitor_id: str, link_id: str) -> None:
        self._client.request(
            "POST",
            f"/api/v1/teams/{team_id}/monitors/{monitor_id}/external-links/{link_id}",
        )

    def unassign(self, team_id: str, monitor_id: str, link_id: str) -> None:
        self._client.request(
            "DELETE",
            f"/api/v1/teams/{team_id}/monitors/{monitor_id}/external-links/{link_id}",
        )

    def list_monitor_links(self, team_id: str, monitor_id: str) -> list[ExternalLink]:
        resp = self._client.request("GET", f"/api/v1/teams/{team_id}/monitors/{monitor_id}/external-links")
        return [ExternalLink.model_validate(lnk) for lnk in json.loads(resp)]
