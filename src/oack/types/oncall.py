"""On-call types."""

from __future__ import annotations

from pydantic import BaseModel


class OnCallSchedule(BaseModel):
    id: str
    account_id: str
    name: str
    timezone: str = ""
    rotation_type: str = ""
    participants: list[str] = []
    handoff_time: str = ""
    handoff_day: int = 0
    created_at: str = ""
    updated_at: str = ""


class CreateScheduleParams(BaseModel):
    name: str
    timezone: str | None = None
    rotation_type: str | None = None
    participants: list[str] | None = None
    handoff_time: str | None = None
    handoff_day: int | None = None


class UpdateScheduleParams(BaseModel):
    name: str | None = None
    timezone: str | None = None
    rotation_type: str | None = None
    participants: list[str] | None = None
    handoff_time: str | None = None
    handoff_day: int | None = None


class OnCallOverride(BaseModel):
    id: str
    schedule_id: str
    original_user_id: str = ""
    replacement_user_id: str = ""
    start_at: str = ""
    end_at: str = ""
    reason: str = ""
    created_at: str = ""


class CreateOverrideParams(BaseModel):
    original_user_id: str
    replacement_user_id: str
    start_at: str
    end_at: str
    reason: str | None = None


class WhosOnCall(BaseModel):
    schedule_id: str
    schedule_name: str = ""
    user_id: str = ""
    override_id: str = ""
