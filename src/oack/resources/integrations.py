"""Integration resource."""

from __future__ import annotations

import json
from typing import TYPE_CHECKING

from oack.types.integrations import CFIntegration, PDIntegration

if TYPE_CHECKING:
    from oack._client import AsyncBaseClient, BaseClient


class AsyncIntegrations:
    def __init__(self, client: AsyncBaseClient) -> None:
        self._client = client

    # --- PagerDuty ---

    async def create_pagerduty(self, account_id: str, params: dict) -> PDIntegration:
        resp = await self._client.request("POST", f"/api/v1/accounts/{account_id}/integrations/pagerduty", json=params)
        return PDIntegration.model_validate_json(resp)

    async def get_pagerduty(self, account_id: str) -> PDIntegration:
        resp = await self._client.request("GET", f"/api/v1/accounts/{account_id}/integrations/pagerduty")
        return PDIntegration.model_validate_json(resp)

    async def update_pagerduty(self, account_id: str, params: dict) -> PDIntegration:
        resp = await self._client.request("PUT", f"/api/v1/accounts/{account_id}/integrations/pagerduty", json=params)
        return PDIntegration.model_validate_json(resp)

    async def delete_pagerduty(self, account_id: str) -> None:
        await self._client.request("DELETE", f"/api/v1/accounts/{account_id}/integrations/pagerduty")

    async def sync_pagerduty(self, account_id: str) -> PDIntegration:
        resp = await self._client.request("POST", f"/api/v1/accounts/{account_id}/integrations/pagerduty/sync")
        return PDIntegration.model_validate_json(resp)

    # --- Cloudflare ---

    async def create_cloudflare(self, account_id: str, params: dict) -> CFIntegration:
        resp = await self._client.request(
            "POST", f"/api/v1/accounts/{account_id}/integrations/cloudflare-zone", json=params
        )
        return CFIntegration.model_validate_json(resp)

    async def list_cloudflare(self, account_id: str) -> list[CFIntegration]:
        resp = await self._client.request("GET", f"/api/v1/accounts/{account_id}/integrations/cloudflare-zone")
        return [CFIntegration.model_validate(c) for c in json.loads(resp)]

    async def update_cloudflare(self, account_id: str, cf_id: str, api_token: str) -> CFIntegration:
        resp = await self._client.request(
            "PUT",
            f"/api/v1/accounts/{account_id}/integrations/cloudflare-zone/{cf_id}",
            json={"api_token": api_token},
        )
        return CFIntegration.model_validate_json(resp)

    async def delete_cloudflare(self, account_id: str, cf_id: str) -> None:
        await self._client.request("DELETE", f"/api/v1/accounts/{account_id}/integrations/cloudflare-zone/{cf_id}")


class Integrations:
    def __init__(self, client: BaseClient) -> None:
        self._client = client

    # --- PagerDuty ---

    def create_pagerduty(self, account_id: str, params: dict) -> PDIntegration:
        resp = self._client.request("POST", f"/api/v1/accounts/{account_id}/integrations/pagerduty", json=params)
        return PDIntegration.model_validate_json(resp)

    def get_pagerduty(self, account_id: str) -> PDIntegration:
        resp = self._client.request("GET", f"/api/v1/accounts/{account_id}/integrations/pagerduty")
        return PDIntegration.model_validate_json(resp)

    def update_pagerduty(self, account_id: str, params: dict) -> PDIntegration:
        resp = self._client.request("PUT", f"/api/v1/accounts/{account_id}/integrations/pagerduty", json=params)
        return PDIntegration.model_validate_json(resp)

    def delete_pagerduty(self, account_id: str) -> None:
        self._client.request("DELETE", f"/api/v1/accounts/{account_id}/integrations/pagerduty")

    def sync_pagerduty(self, account_id: str) -> PDIntegration:
        resp = self._client.request("POST", f"/api/v1/accounts/{account_id}/integrations/pagerduty/sync")
        return PDIntegration.model_validate_json(resp)

    # --- Cloudflare ---

    def create_cloudflare(self, account_id: str, params: dict) -> CFIntegration:
        resp = self._client.request("POST", f"/api/v1/accounts/{account_id}/integrations/cloudflare-zone", json=params)
        return CFIntegration.model_validate_json(resp)

    def list_cloudflare(self, account_id: str) -> list[CFIntegration]:
        resp = self._client.request("GET", f"/api/v1/accounts/{account_id}/integrations/cloudflare-zone")
        return [CFIntegration.model_validate(c) for c in json.loads(resp)]

    def update_cloudflare(self, account_id: str, cf_id: str, api_token: str) -> CFIntegration:
        resp = self._client.request(
            "PUT",
            f"/api/v1/accounts/{account_id}/integrations/cloudflare-zone/{cf_id}",
            json={"api_token": api_token},
        )
        return CFIntegration.model_validate_json(resp)

    def delete_cloudflare(self, account_id: str, cf_id: str) -> None:
        self._client.request("DELETE", f"/api/v1/accounts/{account_id}/integrations/cloudflare-zone/{cf_id}")
