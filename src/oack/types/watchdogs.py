"""Watchdog types."""

from __future__ import annotations

from pydantic import BaseModel


class Watchdog(BaseModel):
    id: str
    component_id: str
    monitor_id: str
    severity: str
    auto_create: bool
    auto_resolve: bool
    notify_subscribers: bool
    template_id: str = ""
    created_at: str


class CreateWatchdogParams(BaseModel):
    monitor_id: str
    severity: str
    auto_create: bool | None = None
    auto_resolve: bool | None = None
    notify_subscribers: bool | None = None
    template_id: str | None = None


class UpdateWatchdogParams(BaseModel):
    severity: str | None = None
    auto_create: bool | None = None
    auto_resolve: bool | None = None
    notify_subscribers: bool | None = None
    template_id: str | None = None
