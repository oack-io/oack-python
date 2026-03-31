"""Escalation policy resource."""

from __future__ import annotations

import json
from typing import TYPE_CHECKING

from oack.types.escalation_policies import (
    CreateEscalationPolicyParams,
    EscalationPolicy,
    UpdateEscalationPolicyParams,
)

if TYPE_CHECKING:
    from oack._client import AsyncBaseClient, BaseClient


def _base_path(account_id: str) -> str:
    return f"/api/v1/accounts/{account_id}/oncall/escalation-policies"


def _policy_path(account_id: str, policy_id: str) -> str:
    return f"{_base_path(account_id)}/{policy_id}"


class AsyncEscalationPolicies:
    def __init__(self, client: AsyncBaseClient) -> None:
        self._client = client

    async def create(self, account_id: str, params: CreateEscalationPolicyParams) -> EscalationPolicy:
        resp = await self._client.request("POST", _base_path(account_id), json=params.model_dump(exclude_none=True))
        return EscalationPolicy.model_validate_json(resp)

    async def list(self, account_id: str) -> list[EscalationPolicy]:
        resp = await self._client.request("GET", _base_path(account_id))
        return [EscalationPolicy.model_validate(p) for p in json.loads(resp)]

    async def update(self, account_id: str, policy_id: str, params: UpdateEscalationPolicyParams) -> EscalationPolicy:
        resp = await self._client.request(
            "PUT",
            _policy_path(account_id, policy_id),
            json=params.model_dump(exclude_none=True),
        )
        return EscalationPolicy.model_validate_json(resp)

    async def delete(self, account_id: str, policy_id: str) -> None:
        await self._client.request("DELETE", _policy_path(account_id, policy_id))


class EscalationPolicies:
    def __init__(self, client: BaseClient) -> None:
        self._client = client

    def create(self, account_id: str, params: CreateEscalationPolicyParams) -> EscalationPolicy:
        resp = self._client.request("POST", _base_path(account_id), json=params.model_dump(exclude_none=True))
        return EscalationPolicy.model_validate_json(resp)

    def list(self, account_id: str) -> list[EscalationPolicy]:
        resp = self._client.request("GET", _base_path(account_id))
        return [EscalationPolicy.model_validate(p) for p in json.loads(resp)]

    def update(self, account_id: str, policy_id: str, params: UpdateEscalationPolicyParams) -> EscalationPolicy:
        resp = self._client.request(
            "PUT",
            _policy_path(account_id, policy_id),
            json=params.model_dump(exclude_none=True),
        )
        return EscalationPolicy.model_validate_json(resp)

    def delete(self, account_id: str, policy_id: str) -> None:
        self._client.request("DELETE", _policy_path(account_id, policy_id))
