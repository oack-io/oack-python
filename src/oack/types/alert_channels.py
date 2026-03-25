"""Alert channel types."""

from __future__ import annotations

from pydantic import BaseModel


class AlertChannel(BaseModel):
    id: str
    team_id: str
    type: str
    name: str
    config: dict[str, str]
    enabled: bool
    email_verified: bool
    scope: str
    created_at: str
    updated_at: str


class CreateAlertChannelParams(BaseModel):
    type: str
    name: str
    config: dict[str, str]
    enabled: bool | None = None


class AlertEvent(BaseModel):
    id: str
    monitor_id: str
    channel_id: str
    type: str
    message: str
    delivered: bool
    error: str
    created_at: str


class MonitorChannelsResponse(BaseModel):
    channel_ids: list[str]
