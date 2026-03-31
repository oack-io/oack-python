"""On-call resource."""

from __future__ import annotations

import json
from typing import TYPE_CHECKING

from oack.types.oncall import (
    CreateOverrideParams,
    CreateScheduleParams,
    OnCallOverride,
    OnCallSchedule,
    UpdateScheduleParams,
    WhosOnCall,
)

if TYPE_CHECKING:
    from oack._client import AsyncBaseClient, BaseClient


def _schedule_base(account_id: str) -> str:
    return f"/api/v1/accounts/{account_id}/oncall/schedules"


def _schedule_path(account_id: str, schedule_id: str) -> str:
    return f"{_schedule_base(account_id)}/{schedule_id}"


class AsyncOnCall:
    def __init__(self, client: AsyncBaseClient) -> None:
        self._client = client

    # ── Schedules ──────────────────────────────────────────────────────

    async def create_schedule(self, account_id: str, params: CreateScheduleParams) -> OnCallSchedule:
        resp = await self._client.request("POST", _schedule_base(account_id), json=params.model_dump(exclude_none=True))
        return OnCallSchedule.model_validate_json(resp)

    async def get_schedule(self, account_id: str, schedule_id: str) -> OnCallSchedule:
        resp = await self._client.request("GET", _schedule_path(account_id, schedule_id))
        return OnCallSchedule.model_validate_json(resp)

    async def list_schedules(self, account_id: str) -> list[OnCallSchedule]:
        resp = await self._client.request("GET", _schedule_base(account_id))
        return [OnCallSchedule.model_validate(s) for s in json.loads(resp)]

    async def update_schedule(self, account_id: str, schedule_id: str, params: UpdateScheduleParams) -> OnCallSchedule:
        resp = await self._client.request(
            "PUT",
            _schedule_path(account_id, schedule_id),
            json=params.model_dump(exclude_none=True),
        )
        return OnCallSchedule.model_validate_json(resp)

    async def delete_schedule(self, account_id: str, schedule_id: str) -> None:
        await self._client.request("DELETE", _schedule_path(account_id, schedule_id))

    # ── Overrides ──────────────────────────────────────────────────────

    async def create_override(self, account_id: str, schedule_id: str, params: CreateOverrideParams) -> OnCallOverride:
        resp = await self._client.request(
            "POST",
            f"{_schedule_path(account_id, schedule_id)}/overrides",
            json=params.model_dump(exclude_none=True),
        )
        return OnCallOverride.model_validate_json(resp)

    async def list_overrides(self, account_id: str, schedule_id: str) -> list[OnCallOverride]:
        resp = await self._client.request("GET", f"{_schedule_path(account_id, schedule_id)}/overrides")
        return [OnCallOverride.model_validate(o) for o in json.loads(resp)]

    async def delete_override(self, account_id: str, schedule_id: str, override_id: str) -> None:
        await self._client.request(
            "DELETE",
            f"{_schedule_path(account_id, schedule_id)}/overrides/{override_id}",
        )

    # ── Who's on call ──────────────────────────────────────────────────

    async def whos_on_call(self, account_id: str) -> list[WhosOnCall]:
        resp = await self._client.request("GET", f"/api/v1/accounts/{account_id}/oncall/now")
        return [WhosOnCall.model_validate(w) for w in json.loads(resp)]


class OnCall:
    def __init__(self, client: BaseClient) -> None:
        self._client = client

    # ── Schedules ──────────────────────────────────────────────────────

    def create_schedule(self, account_id: str, params: CreateScheduleParams) -> OnCallSchedule:
        resp = self._client.request("POST", _schedule_base(account_id), json=params.model_dump(exclude_none=True))
        return OnCallSchedule.model_validate_json(resp)

    def get_schedule(self, account_id: str, schedule_id: str) -> OnCallSchedule:
        resp = self._client.request("GET", _schedule_path(account_id, schedule_id))
        return OnCallSchedule.model_validate_json(resp)

    def list_schedules(self, account_id: str) -> list[OnCallSchedule]:
        resp = self._client.request("GET", _schedule_base(account_id))
        return [OnCallSchedule.model_validate(s) for s in json.loads(resp)]

    def update_schedule(self, account_id: str, schedule_id: str, params: UpdateScheduleParams) -> OnCallSchedule:
        resp = self._client.request(
            "PUT",
            _schedule_path(account_id, schedule_id),
            json=params.model_dump(exclude_none=True),
        )
        return OnCallSchedule.model_validate_json(resp)

    def delete_schedule(self, account_id: str, schedule_id: str) -> None:
        self._client.request("DELETE", _schedule_path(account_id, schedule_id))

    # ── Overrides ──────────────────────────────────────────────────────

    def create_override(self, account_id: str, schedule_id: str, params: CreateOverrideParams) -> OnCallOverride:
        resp = self._client.request(
            "POST",
            f"{_schedule_path(account_id, schedule_id)}/overrides",
            json=params.model_dump(exclude_none=True),
        )
        return OnCallOverride.model_validate_json(resp)

    def list_overrides(self, account_id: str, schedule_id: str) -> list[OnCallOverride]:
        resp = self._client.request("GET", f"{_schedule_path(account_id, schedule_id)}/overrides")
        return [OnCallOverride.model_validate(o) for o in json.loads(resp)]

    def delete_override(self, account_id: str, schedule_id: str, override_id: str) -> None:
        self._client.request(
            "DELETE",
            f"{_schedule_path(account_id, schedule_id)}/overrides/{override_id}",
        )

    # ── Who's on call ──────────────────────────────────────────────────

    def whos_on_call(self, account_id: str) -> list[WhosOnCall]:
        resp = self._client.request("GET", f"/api/v1/accounts/{account_id}/oncall/now")
        return [WhosOnCall.model_validate(w) for w in json.loads(resp)]
