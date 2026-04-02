"""Monitor types."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel


class BrowserStep(BaseModel):
    action: str
    selector: str | None = None
    value: str | None = None
    url: str | None = None
    attribute: str | None = None
    variable_name: str | None = None
    name: str | None = None
    timeout_ms: int | None = None
    wait_ms: int | None = None


class ScriptEnvVar(BaseModel):
    key: str
    value: str
    secret: bool


class BrowserConfig(BaseModel):
    screenshot_enabled: bool = True
    screenshot_full_page: bool = False
    console_error_threshold: int = 0
    resource_error_threshold: int = 5
    user_agent: str = ""
    viewport_width: int = 1920
    viewport_height: int = 1080
    wait_until: str = "load"
    extra_wait_ms: int = 0
    mode: str | None = None
    steps: list[BrowserStep] | None = None
    script: str | None = None
    script_env: list[ScriptEnvVar] | None = None
    suite_url: str | None = None
    deps_url: str | None = None
    deps_hash: str | None = None
    pw_project: str | None = None
    pw_grep: str | None = None
    pw_tag: str | None = None
    suite_git_sha: str | None = None
    suite_git_branch: str | None = None
    suite_git_origin: str | None = None
    suite_deploy_host: str | None = None
    suite_uploaded_at: str | None = None
    suite_deployed_by_id: str | None = None
    suite_deployed_by: str | None = None
    suite_deployed_by_img: str | None = None
    suite_deploy_cmd: str | None = None


class MonitorLocation(BaseModel):
    id: str
    label: str
    checker_region: str | None = None
    checker_id: str | None = None
    assigned_checker_id: str | None = None
    health_status: str = ""
    health_down_reason: str = ""
    health_changed_at: str | None = None


class LocationParams(BaseModel):
    checker_id: str | None = None
    checker_region: str | None = None
    label: str | None = None


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
    aggregate_failure_mode: str | None = None
    aggregate_failure_count: int | None = None
    locations: list[MonitorLocation] | None = None
    type: str = "http"
    browser_config: BrowserConfig | None = None


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
    locations: list[LocationParams] | None = None
    aggregate_failure_mode: str | None = None
    aggregate_failure_count: int | None = None
    type: str | None = None
    browser_config: BrowserConfig | None = None

    def to_request_body(self) -> dict[str, Any]:
        return self.model_dump(exclude_none=True)
