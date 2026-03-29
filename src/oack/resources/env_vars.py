"""Environment variable resource."""

from __future__ import annotations

import json
from typing import TYPE_CHECKING

from oack.types.env_vars import CreateEnvVarParams, EnvVar, UpdateEnvVarParams

if TYPE_CHECKING:
    from oack._client import AsyncBaseClient, BaseClient


def _env_path(team_id: str) -> str:
    return f"/api/v1/teams/{team_id}/env"


class AsyncEnvVars:
    def __init__(self, client: AsyncBaseClient) -> None:
        self._client = client

    async def list(self, team_id: str) -> list[EnvVar]:
        resp = await self._client.request("GET", _env_path(team_id))
        return [EnvVar.model_validate(v) for v in json.loads(resp)]

    async def create(self, team_id: str, params: CreateEnvVarParams) -> EnvVar:
        resp = await self._client.request("POST", _env_path(team_id), json=params.model_dump())
        return EnvVar.model_validate_json(resp)

    async def update(self, team_id: str, key: str, params: UpdateEnvVarParams) -> EnvVar:
        resp = await self._client.request("PUT", f"{_env_path(team_id)}/{key}", json=params.model_dump())
        return EnvVar.model_validate_json(resp)

    async def delete(self, team_id: str, key: str) -> None:
        await self._client.request("DELETE", f"{_env_path(team_id)}/{key}")


class EnvVars:
    def __init__(self, client: BaseClient) -> None:
        self._client = client

    def list(self, team_id: str) -> list[EnvVar]:
        resp = self._client.request("GET", _env_path(team_id))
        return [EnvVar.model_validate(v) for v in json.loads(resp)]

    def create(self, team_id: str, params: CreateEnvVarParams) -> EnvVar:
        resp = self._client.request("POST", _env_path(team_id), json=params.model_dump())
        return EnvVar.model_validate_json(resp)

    def update(self, team_id: str, key: str, params: UpdateEnvVarParams) -> EnvVar:
        resp = self._client.request("PUT", f"{_env_path(team_id)}/{key}", json=params.model_dump())
        return EnvVar.model_validate_json(resp)

    def delete(self, team_id: str, key: str) -> None:
        self._client.request("DELETE", f"{_env_path(team_id)}/{key}")
