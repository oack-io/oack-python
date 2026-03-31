"""Service types."""

from __future__ import annotations

from pydantic import BaseModel


class Service(BaseModel):
    id: str
    account_id: str
    name: str
    description: str = ""
    integration_key: str = ""
    escalation_policy_id: str = ""
    status: str = ""
    tags: list[str] = []
    monitor_ids: list[str] = []
    component_ids: list[str] = []
    dependency_ids: list[str] = []
    dependent_ids: list[str] = []
    created_at: str = ""
    updated_at: str = ""


class CreateServiceParams(BaseModel):
    name: str
    description: str | None = None
    escalation_policy_id: str | None = None
    tags: list[str] | None = None
    monitor_ids: list[str] | None = None


class UpdateServiceParams(BaseModel):
    name: str | None = None
    description: str | None = None
    escalation_policy_id: str | None = None
    tags: list[str] | None = None


class ServiceAnalytics(BaseModel):
    mttr_seconds: float | None = None
    mttf_seconds: float | None = None
    incident_count: int = 0
    by_severity: dict[str, int] = {}
    open_action_items: int = 0
    mttr_by_severity: dict[str, float | None] = {}
    uptime_pct: float | None = None
