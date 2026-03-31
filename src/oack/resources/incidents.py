"""Account incident resource."""

from __future__ import annotations

import json
from typing import TYPE_CHECKING
from urllib.parse import urlencode

from oack.types.incidents import (
    AccountIncident,
    AccountIncidentAnalytics,
    AccountIncidentUpdate,
    AccountIncidentWithDetails,
    CreateAccountIncidentParams,
    ListAccountIncidentsParams,
    PostAccountIncidentUpdateParams,
    UpdateAccountIncidentParams,
)

if TYPE_CHECKING:
    from oack._client import AsyncBaseClient, BaseClient


def _base_path(account_id: str) -> str:
    return f"/api/v1/accounts/{account_id}/incidents"


def _incident_path(account_id: str, incident_id: str) -> str:
    return f"{_base_path(account_id)}/{incident_id}"


def _build_list_query(params: ListAccountIncidentsParams | None) -> str:
    if params is None:
        return ""
    q: dict[str, str] = {}
    if params.status is not None:
        q["status"] = params.status
    if params.severity is not None:
        q["severity"] = params.severity
    if params.tag is not None:
        q["tag"] = params.tag
    if params.service_id is not None:
        q["service_id"] = params.service_id
    if params.from_ is not None:
        q["from"] = params.from_
    if params.to is not None:
        q["to"] = params.to
    if params.limit is not None:
        q["limit"] = str(params.limit)
    if params.offset is not None:
        q["offset"] = str(params.offset)
    return f"?{urlencode(q)}" if q else ""


class AsyncAccountIncidents:
    def __init__(self, client: AsyncBaseClient) -> None:
        self._client = client

    async def create(self, account_id: str, params: CreateAccountIncidentParams) -> AccountIncident:
        resp = await self._client.request("POST", _base_path(account_id), json=params.model_dump(exclude_none=True))
        return AccountIncident.model_validate_json(resp)

    async def get(self, account_id: str, incident_id: str) -> AccountIncidentWithDetails:
        resp = await self._client.request("GET", _incident_path(account_id, incident_id))
        return AccountIncidentWithDetails.model_validate_json(resp)

    async def list(self, account_id: str, params: ListAccountIncidentsParams | None = None) -> list[AccountIncident]:
        path = _base_path(account_id) + _build_list_query(params)
        resp = await self._client.request("GET", path)
        return [AccountIncident.model_validate(i) for i in json.loads(resp)]

    async def update(self, account_id: str, incident_id: str, params: UpdateAccountIncidentParams) -> AccountIncident:
        resp = await self._client.request(
            "PUT",
            _incident_path(account_id, incident_id),
            json=params.model_dump(exclude_none=True),
        )
        return AccountIncident.model_validate_json(resp)

    async def delete(self, account_id: str, incident_id: str) -> None:
        await self._client.request("DELETE", _incident_path(account_id, incident_id))

    async def post_update(
        self, account_id: str, incident_id: str, params: PostAccountIncidentUpdateParams
    ) -> AccountIncidentUpdate:
        resp = await self._client.request(
            "POST",
            f"{_incident_path(account_id, incident_id)}/updates",
            json=params.model_dump(exclude_none=True),
        )
        return AccountIncidentUpdate.model_validate_json(resp)

    async def acknowledge(self, account_id: str, incident_id: str) -> None:
        await self._client.request("POST", f"{_incident_path(account_id, incident_id)}/acknowledge")

    async def link_monitors(self, account_id: str, incident_id: str, monitor_ids: list[str]) -> None:
        await self._client.request(
            "POST",
            f"{_incident_path(account_id, incident_id)}/monitors",
            json={"monitor_ids": monitor_ids},
        )

    async def unlink_monitor(self, account_id: str, incident_id: str, monitor_id: str) -> None:
        await self._client.request("DELETE", f"{_incident_path(account_id, incident_id)}/monitors/{monitor_id}")

    async def link_status_pages(self, account_id: str, incident_id: str, status_page_ids: list[str]) -> None:
        await self._client.request(
            "POST",
            f"{_incident_path(account_id, incident_id)}/status-pages",
            json={"status_page_ids": status_page_ids},
        )

    async def unlink_status_page(self, account_id: str, incident_id: str, page_id: str) -> None:
        await self._client.request("DELETE", f"{_incident_path(account_id, incident_id)}/status-pages/{page_id}")

    async def get_analytics(
        self,
        account_id: str,
        from_: str | None = None,
        to: str | None = None,
        service_id: str | None = None,
    ) -> AccountIncidentAnalytics:
        q: dict[str, str] = {}
        if from_ is not None:
            q["from"] = from_
        if to is not None:
            q["to"] = to
        if service_id is not None:
            q["service_id"] = service_id
        path = f"{_base_path(account_id)}/analytics"
        if q:
            path += f"?{urlencode(q)}"
        resp = await self._client.request("GET", path)
        return AccountIncidentAnalytics.model_validate_json(resp)


class AccountIncidents:
    def __init__(self, client: BaseClient) -> None:
        self._client = client

    def create(self, account_id: str, params: CreateAccountIncidentParams) -> AccountIncident:
        resp = self._client.request("POST", _base_path(account_id), json=params.model_dump(exclude_none=True))
        return AccountIncident.model_validate_json(resp)

    def get(self, account_id: str, incident_id: str) -> AccountIncidentWithDetails:
        resp = self._client.request("GET", _incident_path(account_id, incident_id))
        return AccountIncidentWithDetails.model_validate_json(resp)

    def list(self, account_id: str, params: ListAccountIncidentsParams | None = None) -> list[AccountIncident]:
        path = _base_path(account_id) + _build_list_query(params)
        resp = self._client.request("GET", path)
        return [AccountIncident.model_validate(i) for i in json.loads(resp)]

    def update(self, account_id: str, incident_id: str, params: UpdateAccountIncidentParams) -> AccountIncident:
        resp = self._client.request(
            "PUT",
            _incident_path(account_id, incident_id),
            json=params.model_dump(exclude_none=True),
        )
        return AccountIncident.model_validate_json(resp)

    def delete(self, account_id: str, incident_id: str) -> None:
        self._client.request("DELETE", _incident_path(account_id, incident_id))

    def post_update(
        self, account_id: str, incident_id: str, params: PostAccountIncidentUpdateParams
    ) -> AccountIncidentUpdate:
        resp = self._client.request(
            "POST",
            f"{_incident_path(account_id, incident_id)}/updates",
            json=params.model_dump(exclude_none=True),
        )
        return AccountIncidentUpdate.model_validate_json(resp)

    def acknowledge(self, account_id: str, incident_id: str) -> None:
        self._client.request("POST", f"{_incident_path(account_id, incident_id)}/acknowledge")

    def link_monitors(self, account_id: str, incident_id: str, monitor_ids: list[str]) -> None:
        self._client.request(
            "POST",
            f"{_incident_path(account_id, incident_id)}/monitors",
            json={"monitor_ids": monitor_ids},
        )

    def unlink_monitor(self, account_id: str, incident_id: str, monitor_id: str) -> None:
        self._client.request("DELETE", f"{_incident_path(account_id, incident_id)}/monitors/{monitor_id}")

    def link_status_pages(self, account_id: str, incident_id: str, status_page_ids: list[str]) -> None:
        self._client.request(
            "POST",
            f"{_incident_path(account_id, incident_id)}/status-pages",
            json={"status_page_ids": status_page_ids},
        )

    def unlink_status_page(self, account_id: str, incident_id: str, page_id: str) -> None:
        self._client.request("DELETE", f"{_incident_path(account_id, incident_id)}/status-pages/{page_id}")

    def get_analytics(
        self,
        account_id: str,
        from_: str | None = None,
        to: str | None = None,
        service_id: str | None = None,
    ) -> AccountIncidentAnalytics:
        q: dict[str, str] = {}
        if from_ is not None:
            q["from"] = from_
        if to is not None:
            q["to"] = to
        if service_id is not None:
            q["service_id"] = service_id
        path = f"{_base_path(account_id)}/analytics"
        if q:
            path += f"?{urlencode(q)}"
        resp = self._client.request("GET", path)
        return AccountIncidentAnalytics.model_validate_json(resp)
