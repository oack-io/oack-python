"""Browser probe types."""

from __future__ import annotations

from pydantic import BaseModel


class ConsoleMessage(BaseModel):
    type: str
    text: str
    url: str = ""
    line: int = 0
    column: int = 0


class StepResult(BaseModel):
    action: str
    name: str | None = None
    status: str
    duration_ms: int
    error: str | None = None
    screenshot_url: str | None = None


class BrowserProbe(BaseModel):
    id: str
    checker_id: str | None = None
    checker_public_ip: str | None = None
    status: int
    error: str = ""
    total_ms: int
    dom_content_loaded_ms: int = 0
    load_event_ms: int = 0
    dom_interactive_ms: int = 0
    lcp_ms: float = 0
    fcp_ms: float = 0
    cls: float = 0
    ttfb_ms: float = 0
    resource_count: int = 0
    resource_error_count: int = 0
    resource_total_bytes: int = 0
    resource_status_1xx: int | None = None
    resource_status_2xx: int | None = None
    resource_status_3xx: int | None = None
    resource_status_4xx: int | None = None
    resource_status_5xx: int | None = None
    har_url: str | None = None
    console_error_count: int = 0
    console_warning_count: int = 0
    console_messages: list[ConsoleMessage] | None = None
    screenshot_url: str | None = None
    user_agent: str | None = None
    step_results: list[StepResult] | None = None
    checked_at: str = ""


class BrowserProbeList(BaseModel):
    items: list[BrowserProbe]


class BrowserProbeAggBucket(BaseModel):
    timestamp: str
    probe_count: int = 0
    error_count: int = 0
    total_ms: float = 0
    lcp_ms: float = 0
    fcp_ms: float = 0
    cls: float = 0
    ttfb_ms: float = 0
    resource_count: float = 0
    resource_error_count: float = 0


class BrowserProbeAggregation(BaseModel):
    buckets: list[BrowserProbeAggBucket]
