"""Monitor types."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel


class Monitor(BaseModel):
    id: str
    team_id: str
    name: str
    url: str
    status: str
    timeout_ms: int
    check_interval_ms: int
    http_method: str
    http_version: str
    headers: dict[str, str]
    follow_redirects: bool
    allowed_status_codes: list[str]
    failure_threshold: int
    latency_threshold_ms: int
    ssl_expiry_enabled: bool
    ssl_expiry_thresholds: list[int]
    domain_expiry_enabled: bool
    domain_expiry_thresholds: list[int]
    uptime_threshold_good: float
    uptime_threshold_degraded: float
    uptime_threshold_critical: float
    checker_region: str
    checker_country: str
    resolve_override_ip: str
    health_status: str
    health_down_reason: str
    consecutive_failures: int
    consecutive_successes: int
    health_changed_at: str | None = None
    is_debug_enabled: bool
    debug_expires_at: str | None = None
    checker_id: str
    cf_zone_integration_id: str
    created_by: str
    created_at: str
    updated_at: str


class CreateMonitorParams(BaseModel):
    """Parameters for creating or updating a monitor."""

    name: str
    url: str
    check_interval_ms: int | None = None
    timeout_ms: int | None = None
    http_method: str | None = None
    http_version: str | None = None
    headers: dict[str, str] | None = None
    follow_redirects: bool | None = None
    allowed_status_codes: list[str] | None = None
    failure_threshold: int | None = None
    latency_threshold_ms: int | None = None
    ssl_expiry_enabled: bool | None = None
    ssl_expiry_thresholds: list[int] | None = None
    domain_expiry_enabled: bool | None = None
    domain_expiry_thresholds: list[int] | None = None
    uptime_threshold_good: float | None = None
    uptime_threshold_degraded: float | None = None
    uptime_threshold_critical: float | None = None
    checker_region: str | None = None
    checker_country: str | None = None
    resolve_override_ip: str | None = None
    status: str | None = None

    def to_request_body(self) -> dict[str, Any]:
        return self.model_dump(exclude_none=True)
