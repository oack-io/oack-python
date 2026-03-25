"""Trace types."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel


class Trace(BaseModel):
    id: str
    monitor_id: str
    status: str
    result: Any = None
    requested_by: str = ""
    completed_at: str | None = None
    created_at: str
