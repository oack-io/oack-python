"""Environment variable types."""

from __future__ import annotations

from pydantic import BaseModel


class EnvVar(BaseModel):
    id: str
    team_id: str
    key: str
    value: str
    is_secret: bool
    created_at: str
    updated_at: str


class CreateEnvVarParams(BaseModel):
    key: str
    value: str
    is_secret: bool = False


class UpdateEnvVarParams(BaseModel):
    value: str
    is_secret: bool = False
