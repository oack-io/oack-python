"""Notification types."""

from __future__ import annotations

from pydantic import BaseModel


class NotificationDefaults(BaseModel):
    channel_ids: list[str]


class MonitorNotification(BaseModel):
    monitor_id: str
    channel_ids: list[str]
