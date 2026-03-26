"""User types."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class User(BaseModel):
    id: str
    email: str
    name: str
    email_verified: bool = False
    role: str = ""
    provider: str = ""
    avatar: str = ""
    avatar_url: str = ""
    created_at: str


class Preferences(BaseModel):
    model_config = ConfigDict(extra="allow")

    timezone: str = ""
    date_format: str = ""
    time_format: str = ""
    theme: str = ""


class Device(BaseModel):
    token: str
    platform: str
    created_at: str


class TelegramLink(BaseModel):
    code: str
    url: str
    status: str


class TelegramLinkStatus(BaseModel):
    code: str
    status: str
    linked: bool = False
