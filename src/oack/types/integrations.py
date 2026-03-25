"""Integration types."""

from __future__ import annotations

from pydantic import BaseModel


class PDIntegration(BaseModel):
    id: str
    account_id: str
    api_key: str
    region: str = ""
    service_ids: list[str] = []
    sync_enabled: bool = False
    sync_error: str = ""
    last_synced_at: str | None = None
    enabled: bool
    created_at: str
    updated_at: str


class CFIntegration(BaseModel):
    id: str
    account_id: str
    zone_id: str
    zone_name: str
    api_token: str
    enabled: bool
    session_error: str = ""
    last_connected_at: str | None = None
    created_by: str
    created_at: str
    updated_at: str
