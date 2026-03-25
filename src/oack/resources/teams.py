"""Team resource."""

from __future__ import annotations

import json
from typing import TYPE_CHECKING, Any

from oack.types.teams import AcceptInviteResult, CreateTeamAPIKeyResult, Team, TeamAPIKey, TeamInvite, TeamMember

if TYPE_CHECKING:
    from oack._client import AsyncBaseClient, BaseClient


class AsyncTeams:
    def __init__(self, client: AsyncBaseClient) -> None:
        self._client = client

    async def create(self, account_id: str, name: str) -> Team:
        resp = await self._client.request("POST", f"/api/v1/accounts/{account_id}/teams", json={"name": name})
        return Team.model_validate_json(resp)

    async def list(self) -> list[Team]:
        resp = await self._client.request("GET", "/api/v1/teams")
        return [Team.model_validate(t) for t in json.loads(resp)]

    async def list_by_account(self, account_id: str) -> list[Team]:
        resp = await self._client.request("GET", f"/api/v1/accounts/{account_id}/teams")
        return [Team.model_validate(t) for t in json.loads(resp)]

    async def get(self, team_id: str) -> Team:
        resp = await self._client.request("GET", f"/api/v1/teams/{team_id}")
        return Team.model_validate_json(resp)

    async def update(self, team_id: str, name: str) -> Team:
        resp = await self._client.request("PUT", f"/api/v1/teams/{team_id}", json={"name": name})
        return Team.model_validate_json(resp)

    async def delete(self, team_id: str) -> None:
        await self._client.request("DELETE", f"/api/v1/teams/{team_id}")

    async def list_members(self, team_id: str) -> list[TeamMember]:
        resp = await self._client.request("GET", f"/api/v1/teams/{team_id}/members")
        return [TeamMember.model_validate(m) for m in json.loads(resp)]

    async def add_member(self, team_id: str, user_id: str, role: str) -> TeamMember:
        resp = await self._client.request(
            "POST", f"/api/v1/teams/{team_id}/members", json={"user_id": user_id, "role": role}
        )
        return TeamMember.model_validate_json(resp)

    async def remove_member(self, team_id: str, user_id: str) -> None:
        await self._client.request("DELETE", f"/api/v1/teams/{team_id}/members/{user_id}")

    async def set_member_role(self, team_id: str, user_id: str, role: str) -> None:
        await self._client.request(
            "PUT", f"/api/v1/teams/{team_id}/members/{user_id}/role", json={"role": role}
        )

    async def list_invites(self, team_id: str) -> list[TeamInvite]:
        resp = await self._client.request("GET", f"/api/v1/teams/{team_id}/invites")
        return [TeamInvite.model_validate(i) for i in json.loads(resp)]

    async def create_invite(self, team_id: str) -> TeamInvite:
        resp = await self._client.request("POST", f"/api/v1/teams/{team_id}/invites")
        return TeamInvite.model_validate_json(resp)

    async def revoke_invite(self, team_id: str, invite_id: str) -> None:
        await self._client.request("DELETE", f"/api/v1/teams/{team_id}/invites/{invite_id}")

    async def accept_invite(self, token: str) -> AcceptInviteResult:
        resp = await self._client.request("POST", f"/api/v1/invites/{token}/accept")
        return AcceptInviteResult.model_validate_json(resp)

    async def create_api_key(self, team_id: str, name: str, expires_at: str | None = None) -> CreateTeamAPIKeyResult:
        body: dict[str, Any] = {"name": name}
        if expires_at is not None:
            body["expires_at"] = expires_at
        resp = await self._client.request("POST", f"/api/v1/teams/{team_id}/api-keys", json=body)
        return CreateTeamAPIKeyResult.model_validate_json(resp)

    async def list_api_keys(self, team_id: str) -> list[TeamAPIKey]:
        resp = await self._client.request("GET", f"/api/v1/teams/{team_id}/api-keys")
        return [TeamAPIKey.model_validate(k) for k in json.loads(resp)]

    async def delete_api_key(self, team_id: str, key_id: str) -> None:
        await self._client.request("DELETE", f"/api/v1/teams/{team_id}/api-keys/{key_id}")


class Teams:
    def __init__(self, client: BaseClient) -> None:
        self._client = client

    def create(self, account_id: str, name: str) -> Team:
        resp = self._client.request("POST", f"/api/v1/accounts/{account_id}/teams", json={"name": name})
        return Team.model_validate_json(resp)

    def list(self) -> list[Team]:
        resp = self._client.request("GET", "/api/v1/teams")
        return [Team.model_validate(t) for t in json.loads(resp)]

    def list_by_account(self, account_id: str) -> list[Team]:
        resp = self._client.request("GET", f"/api/v1/accounts/{account_id}/teams")
        return [Team.model_validate(t) for t in json.loads(resp)]

    def get(self, team_id: str) -> Team:
        resp = self._client.request("GET", f"/api/v1/teams/{team_id}")
        return Team.model_validate_json(resp)

    def update(self, team_id: str, name: str) -> Team:
        resp = self._client.request("PUT", f"/api/v1/teams/{team_id}", json={"name": name})
        return Team.model_validate_json(resp)

    def delete(self, team_id: str) -> None:
        self._client.request("DELETE", f"/api/v1/teams/{team_id}")

    def list_members(self, team_id: str) -> list[TeamMember]:
        resp = self._client.request("GET", f"/api/v1/teams/{team_id}/members")
        return [TeamMember.model_validate(m) for m in json.loads(resp)]

    def add_member(self, team_id: str, user_id: str, role: str) -> TeamMember:
        resp = self._client.request(
            "POST", f"/api/v1/teams/{team_id}/members", json={"user_id": user_id, "role": role}
        )
        return TeamMember.model_validate_json(resp)

    def remove_member(self, team_id: str, user_id: str) -> None:
        self._client.request("DELETE", f"/api/v1/teams/{team_id}/members/{user_id}")

    def set_member_role(self, team_id: str, user_id: str, role: str) -> None:
        self._client.request("PUT", f"/api/v1/teams/{team_id}/members/{user_id}/role", json={"role": role})

    def list_invites(self, team_id: str) -> list[TeamInvite]:
        resp = self._client.request("GET", f"/api/v1/teams/{team_id}/invites")
        return [TeamInvite.model_validate(i) for i in json.loads(resp)]

    def create_invite(self, team_id: str) -> TeamInvite:
        resp = self._client.request("POST", f"/api/v1/teams/{team_id}/invites")
        return TeamInvite.model_validate_json(resp)

    def revoke_invite(self, team_id: str, invite_id: str) -> None:
        self._client.request("DELETE", f"/api/v1/teams/{team_id}/invites/{invite_id}")

    def accept_invite(self, token: str) -> AcceptInviteResult:
        resp = self._client.request("POST", f"/api/v1/invites/{token}/accept")
        return AcceptInviteResult.model_validate_json(resp)

    def create_api_key(self, team_id: str, name: str, expires_at: str | None = None) -> CreateTeamAPIKeyResult:
        body: dict[str, Any] = {"name": name}
        if expires_at is not None:
            body["expires_at"] = expires_at
        resp = self._client.request("POST", f"/api/v1/teams/{team_id}/api-keys", json=body)
        return CreateTeamAPIKeyResult.model_validate_json(resp)

    def list_api_keys(self, team_id: str) -> list[TeamAPIKey]:
        resp = self._client.request("GET", f"/api/v1/teams/{team_id}/api-keys")
        return [TeamAPIKey.model_validate(k) for k in json.loads(resp)]

    def delete_api_key(self, team_id: str, key_id: str) -> None:
        self._client.request("DELETE", f"/api/v1/teams/{team_id}/api-keys/{key_id}")
