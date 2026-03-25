"""Account types."""

from __future__ import annotations

from pydantic import BaseModel


class Account(BaseModel):
    id: str
    name: str
    plan: str
    deleted_at: str | None = None
    created_at: str
    updated_at: str


class AccountMember(BaseModel):
    user_id: str
    email: str
    name: str
    avatar_url: str
    role: str
    joined_at: str


class AccountInvite(BaseModel):
    id: str
    account_id: str
    email: str
    role: str
    invited_by: str
    token: str
    invite_url: str
    expires_at: str
    accepted_at: str | None = None
    revoked_at: str | None = None
    created_at: str


class Subscription(BaseModel):
    id: str
    account_id: str
    plan: str
    status: str
    expires_at: str | None = None
    created_at: str
    updated_at: str
