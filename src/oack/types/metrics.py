"""Metrics, timeline, and chart event types."""

from __future__ import annotations

from pydantic import BaseModel


class WindowMetrics(BaseModel):
    uptime: float
    avg_response_ms: float
    p95_response_ms: float
    total_probes: int
    success_probes: int
    failure_probes: int


class MonitorMetrics(BaseModel):
    last_24h: WindowMetrics
    last_7d: WindowMetrics
    last_30d: WindowMetrics


class ExpirationSSL(BaseModel):
    expires_at: str | None = None
    issuer: str
    subject: str
    days_left: int | None = None
    status: str
    checked_at: str | None = None


class ExpirationDomain(BaseModel):
    expires_at: str | None = None
    registrar: str
    days_left: int | None = None
    status: str
    checked_at: str | None = None


class Expiration(BaseModel):
    ssl: ExpirationSSL | None = None
    domain: ExpirationDomain | None = None


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
