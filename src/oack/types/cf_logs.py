"""Cloudflare log types."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from pydantic import BaseModel


class CFLogEntry(BaseModel):
    id: str
    probe_id: str | None = None
    monitor_id: str
    cf_ray: str
    edge_colo_code: str = ""
    cache_status: str = ""
    edge_response_status: int = 0
    origin_response_status: int = 0
    raw_log: dict[str, Any] | None = None
    created_at: str


@dataclass
class CFLogListOptions:
    from_ts: int | None = None
    to_ts: int | None = None
    limit: int | None = None
