"""Geo and checker types."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel


class Checker(BaseModel):
    id: str
    mode: str
    name: str = ""
    public_ip: str = ""
    country: str = ""
    region: str = ""
    latitude: float | None = None
    longitude: float | None = None
    asn: Any = 0
    asn_org: str = ""
    is_online: bool = False
    version: str = ""


class GeoCountry(BaseModel):
    code: str
    name: str


class GeoRegion(BaseModel):
    code: str
    name: str
    countries: list[GeoCountry]
