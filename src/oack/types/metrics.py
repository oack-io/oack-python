"""Metrics, timeline, and chart event types."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class MetricsWindow(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    window_days: int
    from_ts: str | None = Field(None, alias="from")
    to: str | None = None
    uptime_percent: float = 0
    mtbf_seconds: float | None = None
    mttr_seconds: float | None = None
    total_uptime_seconds: int = 0
    total_downtime_seconds: int = 0
    total_excluded_seconds: int = 0
    incident_count: int = 0
    recovery_count: int = 0


class MonitorMetrics(BaseModel):
    monitor_id: str = ""
    current_health: str = ""
    uptime_threshold_good: float = 0
    uptime_threshold_degraded: float = 0
    uptime_threshold_critical: float = 0
    windows: list[MetricsWindow] = []


class ExpirationSSL(BaseModel):
    expires_at: str | None = None
    days_remaining: int | None = None
    issuer: str = ""
    error: str | None = None


class ExpirationDomain(BaseModel):
    expires_at: str | None = None
    days_remaining: int | None = None
    registrar: str = ""
    error: str | None = None


class Expiration(BaseModel):
    domain: str = ""
    ssl: ExpirationSSL | None = None
    domain_registration: ExpirationDomain | None = None


class TimelineEvent(BaseModel):
    id: str
    monitor_id: str
    type: str
    message: str
    created_at: str


class ChartEvent(BaseModel):
    id: str
    team_id: str
    monitor_id: str | None = None
    kind: str
    source: str
    title: str
    body: str
    start_at: str
    end_at: str | None = None
    created_at: str


class CreateChartEventParams(BaseModel):
    monitor_id: str | None = None
    kind: str
    source: str
    title: str
    body: str = ""
    start_at: str
    end_at: str | None = None


class UpdateChartEventParams(BaseModel):
    kind: str | None = None
    source: str | None = None
    title: str | None = None
    body: str | None = None
    start_at: str | None = None
    end_at: str | None = None
