"""Geo resource."""

from __future__ import annotations

import json
from typing import TYPE_CHECKING

from oack.types.geo import Checker, GeoRegion

if TYPE_CHECKING:
    from oack._client import AsyncBaseClient, BaseClient


class AsyncGeo:
    def __init__(self, client: AsyncBaseClient) -> None:
        self._client = client

    async def list_checkers(self) -> list[Checker]:
        resp = await self._client.request("GET", "/api/v1/checkers")
        return [Checker.model_validate(c) for c in json.loads(resp)]

    async def list_regions(self) -> list[GeoRegion]:
        resp = await self._client.request("GET", "/api/v1/regions")
        data = json.loads(resp)
        return [GeoRegion.model_validate(r) for r in data.get("regions", [])]


class Geo:
    def __init__(self, client: BaseClient) -> None:
        self._client = client

    def list_checkers(self) -> list[Checker]:
        resp = self._client.request("GET", "/api/v1/checkers")
        return [Checker.model_validate(c) for c in json.loads(resp)]

    def list_regions(self) -> list[GeoRegion]:
        resp = self._client.request("GET", "/api/v1/regions")
        data = json.loads(resp)
        return [GeoRegion.model_validate(r) for r in data.get("regions", [])]
