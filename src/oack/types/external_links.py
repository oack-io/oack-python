"""External link types."""

from __future__ import annotations

from pydantic import BaseModel


class ExternalLink(BaseModel):
    id: str
    team_id: str
    name: str
    url_template: str
    icon_url: str = ""
    time_window_minutes: int = 0
    created_at: str
    updated_at: str
