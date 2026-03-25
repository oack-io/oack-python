"""Team types."""

from __future__ import annotations

from pydantic import BaseModel


class Team(BaseModel):
    id: str
    name: str
    created_at: str
    updated_at: str


class TeamMember(BaseModel):
    user_id: str
    email: str
    name: str
    avatar_url: str
    role: str
    joined_at: str


class TeamInvite(BaseModel):
    id: str
    team_id: str
    token: str
    role: str
    created_by: str
    expires_at: str
    created_at: str


class AcceptInviteResult(BaseModel):
    team_id: str
    team_name: str
    role: str


class TeamAPIKey(BaseModel):
    id: str
    team_id: str
    name: str
    key_prefix: str
    created_by: str
    expires_at: str | None = None
    created_at: str


class CreateTeamAPIKeyResult(BaseModel):
    key: str
    api_key: TeamAPIKey
