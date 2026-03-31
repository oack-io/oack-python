"""Postmortem resource."""

from __future__ import annotations

import json
from typing import TYPE_CHECKING

from oack.types.postmortems import (
    CreateActionItemParams,
    CreatePostmortemParams,
    CreatePostmortemTemplateParams,
    Postmortem,
    PostmortemAction,
    PostmortemTemplate,
    UpdateActionItemParams,
    UpdatePostmortemParams,
    UpdatePostmortemTemplateParams,
)

if TYPE_CHECKING:
    from oack._client import AsyncBaseClient, BaseClient


def _pm_path(account_id: str, incident_id: str) -> str:
    return f"/api/v1/accounts/{account_id}/incidents/{incident_id}/postmortem"


def _template_base(account_id: str) -> str:
    return f"/api/v1/accounts/{account_id}/postmortem-templates"


class AsyncPostmortems:
    def __init__(self, client: AsyncBaseClient) -> None:
        self._client = client

    # ── Postmortem CRUD ────────────────────────────────────────────────

    async def create(self, account_id: str, incident_id: str, params: CreatePostmortemParams) -> Postmortem:
        resp = await self._client.request(
            "POST",
            _pm_path(account_id, incident_id),
            json=params.model_dump(exclude_none=True),
        )
        return Postmortem.model_validate_json(resp)

    async def get(self, account_id: str, incident_id: str) -> Postmortem:
        resp = await self._client.request("GET", _pm_path(account_id, incident_id))
        return Postmortem.model_validate_json(resp)

    async def update(self, account_id: str, incident_id: str, params: UpdatePostmortemParams) -> Postmortem:
        resp = await self._client.request(
            "PUT",
            _pm_path(account_id, incident_id),
            json=params.model_dump(exclude_none=True),
        )
        return Postmortem.model_validate_json(resp)

    async def delete(self, account_id: str, incident_id: str) -> None:
        await self._client.request("DELETE", _pm_path(account_id, incident_id))

    async def publish(self, account_id: str, incident_id: str) -> Postmortem:
        resp = await self._client.request("POST", f"{_pm_path(account_id, incident_id)}/publish")
        return Postmortem.model_validate_json(resp)

    async def generate_share_token(self, account_id: str, incident_id: str) -> str:
        resp = await self._client.request("POST", f"{_pm_path(account_id, incident_id)}/share")
        return json.loads(resp)["share_token"]

    # ── Action Items ───────────────────────────────────────────────────

    async def create_action_item(
        self, account_id: str, incident_id: str, params: CreateActionItemParams
    ) -> PostmortemAction:
        resp = await self._client.request(
            "POST",
            f"{_pm_path(account_id, incident_id)}/action-items",
            json=params.model_dump(exclude_none=True),
        )
        return PostmortemAction.model_validate_json(resp)

    async def update_action_item(
        self,
        account_id: str,
        incident_id: str,
        item_id: str,
        params: UpdateActionItemParams,
    ) -> PostmortemAction:
        resp = await self._client.request(
            "PUT",
            f"{_pm_path(account_id, incident_id)}/action-items/{item_id}",
            json=params.model_dump(exclude_none=True),
        )
        return PostmortemAction.model_validate_json(resp)

    async def delete_action_item(self, account_id: str, incident_id: str, item_id: str) -> None:
        await self._client.request("DELETE", f"{_pm_path(account_id, incident_id)}/action-items/{item_id}")

    # ── Templates ──────────────────────────────────────────────────────

    async def create_template(self, account_id: str, params: CreatePostmortemTemplateParams) -> PostmortemTemplate:
        resp = await self._client.request("POST", _template_base(account_id), json=params.model_dump(exclude_none=True))
        return PostmortemTemplate.model_validate_json(resp)

    async def list_templates(self, account_id: str) -> list[PostmortemTemplate]:
        resp = await self._client.request("GET", _template_base(account_id))
        return [PostmortemTemplate.model_validate(t) for t in json.loads(resp)]

    async def get_template(self, account_id: str, template_id: str) -> PostmortemTemplate:
        resp = await self._client.request("GET", f"{_template_base(account_id)}/{template_id}")
        return PostmortemTemplate.model_validate_json(resp)

    async def update_template(
        self, account_id: str, template_id: str, params: UpdatePostmortemTemplateParams
    ) -> PostmortemTemplate:
        resp = await self._client.request(
            "PUT",
            f"{_template_base(account_id)}/{template_id}",
            json=params.model_dump(exclude_none=True),
        )
        return PostmortemTemplate.model_validate_json(resp)

    async def delete_template(self, account_id: str, template_id: str) -> None:
        await self._client.request("DELETE", f"{_template_base(account_id)}/{template_id}")


class Postmortems:
    def __init__(self, client: BaseClient) -> None:
        self._client = client

    # ── Postmortem CRUD ────────────────────────────────────────────────

    def create(self, account_id: str, incident_id: str, params: CreatePostmortemParams) -> Postmortem:
        resp = self._client.request(
            "POST",
            _pm_path(account_id, incident_id),
            json=params.model_dump(exclude_none=True),
        )
        return Postmortem.model_validate_json(resp)

    def get(self, account_id: str, incident_id: str) -> Postmortem:
        resp = self._client.request("GET", _pm_path(account_id, incident_id))
        return Postmortem.model_validate_json(resp)

    def update(self, account_id: str, incident_id: str, params: UpdatePostmortemParams) -> Postmortem:
        resp = self._client.request(
            "PUT",
            _pm_path(account_id, incident_id),
            json=params.model_dump(exclude_none=True),
        )
        return Postmortem.model_validate_json(resp)

    def delete(self, account_id: str, incident_id: str) -> None:
        self._client.request("DELETE", _pm_path(account_id, incident_id))

    def publish(self, account_id: str, incident_id: str) -> Postmortem:
        resp = self._client.request("POST", f"{_pm_path(account_id, incident_id)}/publish")
        return Postmortem.model_validate_json(resp)

    def generate_share_token(self, account_id: str, incident_id: str) -> str:
        resp = self._client.request("POST", f"{_pm_path(account_id, incident_id)}/share")
        return json.loads(resp)["share_token"]

    # ── Action Items ───────────────────────────────────────────────────

    def create_action_item(self, account_id: str, incident_id: str, params: CreateActionItemParams) -> PostmortemAction:
        resp = self._client.request(
            "POST",
            f"{_pm_path(account_id, incident_id)}/action-items",
            json=params.model_dump(exclude_none=True),
        )
        return PostmortemAction.model_validate_json(resp)

    def update_action_item(
        self,
        account_id: str,
        incident_id: str,
        item_id: str,
        params: UpdateActionItemParams,
    ) -> PostmortemAction:
        resp = self._client.request(
            "PUT",
            f"{_pm_path(account_id, incident_id)}/action-items/{item_id}",
            json=params.model_dump(exclude_none=True),
        )
        return PostmortemAction.model_validate_json(resp)

    def delete_action_item(self, account_id: str, incident_id: str, item_id: str) -> None:
        self._client.request("DELETE", f"{_pm_path(account_id, incident_id)}/action-items/{item_id}")

    # ── Templates ──────────────────────────────────────────────────────

    def create_template(self, account_id: str, params: CreatePostmortemTemplateParams) -> PostmortemTemplate:
        resp = self._client.request("POST", _template_base(account_id), json=params.model_dump(exclude_none=True))
        return PostmortemTemplate.model_validate_json(resp)

    def list_templates(self, account_id: str) -> list[PostmortemTemplate]:
        resp = self._client.request("GET", _template_base(account_id))
        return [PostmortemTemplate.model_validate(t) for t in json.loads(resp)]

    def get_template(self, account_id: str, template_id: str) -> PostmortemTemplate:
        resp = self._client.request("GET", f"{_template_base(account_id)}/{template_id}")
        return PostmortemTemplate.model_validate_json(resp)

    def update_template(
        self, account_id: str, template_id: str, params: UpdatePostmortemTemplateParams
    ) -> PostmortemTemplate:
        resp = self._client.request(
            "PUT",
            f"{_template_base(account_id)}/{template_id}",
            json=params.model_dump(exclude_none=True),
        )
        return PostmortemTemplate.model_validate_json(resp)

    def delete_template(self, account_id: str, template_id: str) -> None:
        self._client.request("DELETE", f"{_template_base(account_id)}/{template_id}")
