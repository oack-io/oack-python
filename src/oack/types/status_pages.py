"""Status page types."""

from __future__ import annotations

from pydantic import BaseModel


class StatusPage(BaseModel):
    id: str
    account_id: str
    name: str
    slug: str
    custom_domain: str = ""
    is_public: bool = True
    password_enabled: bool = False
    created_at: str
    updated_at: str


class Component(BaseModel):
    id: str
    status_page_id: str
    group_id: str | None = None
    name: str
    description: str = ""
    status: str
    position: int
    created_at: str
    updated_at: str


class ComponentGroup(BaseModel):
    id: str
    status_page_id: str
    name: str
    position: int
    created_at: str
    updated_at: str


class Incident(BaseModel):
    id: str
    status_page_id: str
    title: str
    status: str
    impact: str
    body: str = ""
    created_at: str
    updated_at: str


class IncidentUpdate(BaseModel):
    id: str
    incident_id: str
    status: str
    body: str
    created_at: str


class IncidentTemplate(BaseModel):
    id: str
    status_page_id: str
    title: str
    body: str
    impact: str
    created_at: str
    updated_at: str


class Maintenance(BaseModel):
    id: str
    status_page_id: str
    title: str
    status: str
    body: str = ""
    scheduled_start: str
    scheduled_end: str
    created_at: str
    updated_at: str


class MaintenanceUpdate(BaseModel):
    id: str
    maintenance_id: str
    status: str
    body: str
    created_at: str


class Watchdog(BaseModel):
    id: str
    component_id: str
    monitor_id: str
    team_id: str
    created_at: str


class Subscriber(BaseModel):
    id: str
    status_page_id: str
    email: str
    confirmed: bool
    created_at: str
