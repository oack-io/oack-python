"""Probe types."""

from __future__ import annotations

from pydantic import BaseModel


class Probe(BaseModel):
    id: str
    monitor_id: str
    checker_id: str
    checker_region: str
    checker_country: str
    status_code: int
    response_time_ms: float
    dns_time_ms: float
    connect_time_ms: float
    tls_time_ms: float
    ttfb_ms: float
    transfer_time_ms: float
    error: str
    is_up: bool
    created_at: str


class ProbeList(BaseModel):
    """Wrapper for probe list responses. The API returns a plain array."""

    probes: list[Probe] = []
    total: int = 0

    @classmethod
    def from_response(cls, data: list[dict]) -> ProbeList:
        probes = [Probe.model_validate(p) for p in data]
        return cls(probes=probes, total=len(probes))


class ProbeAggBucket(BaseModel):
    timestamp: str
    avg_response_ms: float
    min_response_ms: float
    max_response_ms: float
    success_count: int
    failure_count: int
    total_count: int


class ProbeAggregation(BaseModel):
    buckets: list[ProbeAggBucket]
