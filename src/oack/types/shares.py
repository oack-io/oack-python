"""Share types."""

from __future__ import annotations

from pydantic import BaseModel


class Share(BaseModel):
    id: str
    token: str
    share_url: str = ""
    monitor_id: str = ""
    from_ts: str | None = None
    to: str | None = None
    access_mode: str = ""
    expires_at: str | None = None
    redacted_groups: list[str] | None = None
    include_comments: bool = False
    view_count: int = 0
    created_at: str = ""


class CreateShareParams(BaseModel):
    from_ts: str | None = None
    to: str | None = None
    access_mode: str | None = None
    expires_in: str | None = None
    redacted_groups: list[str] | None = None
    include_groups: list[str] | None = None
    include_comments: bool | None = None

    def to_request_body(self) -> dict:
        data = self.model_dump(exclude_none=True)
        # API uses "from" not "from_ts"
        if "from_ts" in data:
            data["from"] = data.pop("from_ts")
        return data
