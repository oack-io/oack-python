"""Share types."""

from __future__ import annotations

from pydantic import BaseModel


class Share(BaseModel):
    id: str
    monitor_id: str
    token: str
    share_url: str = ""
    created_by: str
    expires_at: str | None = None
    created_at: str
