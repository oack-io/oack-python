"""Account incident types."""

from __future__ import annotations

from pydantic import BaseModel


class AccountIncident(BaseModel):
    id: str
    account_id: str
    name: str
    status: str = ""
    severity: str = ""
    summary: str = ""
    created_by: str = ""
    owner_id: str = ""
    declared_at: str = ""
    resolved_at: str = ""
    duration_seconds: int | None = None
    is_private: bool = False
    tags: list[str] = []
    source: str = ""
    monitor_ids: list[str] = []
    status_page_ids: list[str] = []
    service_ids: list[str] = []
    escalation_policy_id: str = ""
    created_at: str = ""
    updated_at: str = ""


class AccountIncidentUpdate(BaseModel):
    id: str
    incident_id: str
    status: str = ""
    message: str = ""
    created_by: str = ""
    notify_subscribers: bool = False
    created_at: str = ""


class EscalationState(BaseModel):
    status: str = ""
    current_level: int = 0
    acknowledged_by: str = ""
    acknowledged_at: str = ""


class EscalationEvent(BaseModel):
    level: int = 0
    user_id: str = ""
    schedule_id: str = ""
    trigger: str = ""
    created_at: str = ""


class AccountIncidentWithDetails(AccountIncident):
    updates: list[AccountIncidentUpdate] = []
    escalation_state: EscalationState | None = None
    escalation_events: list[EscalationEvent] = []


class CreateAccountIncidentParams(BaseModel):
    name: str
    severity: str | None = None
    summary: str | None = None
    is_private: bool | None = None
    tags: list[str] | None = None
    monitor_ids: list[str] | None = None
    status_page_ids: list[str] | None = None
    service_ids: list[str] | None = None
    primary_escalation_policy_id: str | None = None
    no_escalation: bool | None = None


class UpdateAccountIncidentParams(BaseModel):
    name: str | None = None
    status: str | None = None
    severity: str | None = None
    summary: str | None = None
    owner_id: str | None = None
    is_private: bool | None = None
    tags: list[str] | None = None


class PostAccountIncidentUpdateParams(BaseModel):
    status: str
    message: str
    notify_subscribers: bool = False


class ListAccountIncidentsParams(BaseModel):
    status: str | None = None
    severity: str | None = None
    tag: str | None = None
    service_id: str | None = None
    from_: str | None = None
    to: str | None = None
    limit: int | None = None
    offset: int | None = None


class AccountIncidentAnalytics(BaseModel):
    mttr_seconds: float | None = None
    mttf_seconds: float | None = None
    incident_count: int = 0
    by_severity: dict[str, int] = {}
    open_action_items: int = 0
    mttr_by_severity: dict[str, float | None] = {}
    uptime_pct: float | None = None
