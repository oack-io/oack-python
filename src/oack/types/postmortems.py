"""Postmortem types."""

from __future__ import annotations

from pydantic import BaseModel


class PostmortemAction(BaseModel):
    id: str
    postmortem_id: str
    title: str = ""
    description: str = ""
    owner_id: str = ""
    status: str = ""
    priority: str = ""
    due_date: str = ""
    completed_at: str = ""
    created_at: str = ""
    updated_at: str = ""


class Postmortem(BaseModel):
    id: str
    incident_id: str
    account_id: str
    status: str = ""
    summary: str = ""
    timeline_md: str = ""
    root_cause_md: str = ""
    impact_md: str = ""
    lessons_md: str = ""
    body_md: str = ""
    share_token: str = ""
    created_by: str = ""
    published_at: str = ""
    action_items: list[PostmortemAction] = []
    created_at: str = ""
    updated_at: str = ""


class CreatePostmortemParams(BaseModel):
    body_md: str | None = None


class UpdatePostmortemParams(BaseModel):
    summary: str | None = None
    timeline_md: str | None = None
    root_cause_md: str | None = None
    impact_md: str | None = None
    lessons_md: str | None = None
    body_md: str | None = None


class CreateActionItemParams(BaseModel):
    title: str
    description: str | None = None
    owner_id: str | None = None
    priority: str | None = None
    due_date: str | None = None


class UpdateActionItemParams(BaseModel):
    title: str | None = None
    description: str | None = None
    owner_id: str | None = None
    status: str | None = None
    priority: str | None = None
    due_date: str | None = None


class PostmortemTemplate(BaseModel):
    id: str
    account_id: str
    name: str
    content: str = ""
    is_default: bool = False
    created_by: str = ""
    created_at: str = ""
    updated_at: str = ""


class CreatePostmortemTemplateParams(BaseModel):
    name: str
    content: str
    is_default: bool = False


class UpdatePostmortemTemplateParams(BaseModel):
    name: str | None = None
    content: str | None = None
    is_default: bool | None = None
