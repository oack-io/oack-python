"""Geo and checker types."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel


class Checker(BaseModel):
    id: str
    region: str
    country: str
    ip: str
    asn: Any
    mode: str
    status: str


class GeoCountry(BaseModel):
    code: str
    name: str


class GeoRegion(BaseModel):
    code: str
    name: str
    countries: list[GeoCountry]
