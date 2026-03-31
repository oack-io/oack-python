"""Escalation policy types."""

from __future__ import annotations

from pydantic import BaseModel


class EscalationLevel(BaseModel):
    schedule_id: str
    ack_timeout_minutes: int | None = None
    duration_minutes: int | None = None


class EscalationPolicy(BaseModel):
    id: str
    account_id: str
    name: str
    levels: list[EscalationLevel] = []
    created_at: str = ""
    updated_at: str = ""


class CreateEscalationPolicyParams(BaseModel):
    name: str
    levels: list[EscalationLevel] | None = None


class UpdateEscalationPolicyParams(BaseModel):
    name: str | None = None
    levels: list[EscalationLevel] | None = None
