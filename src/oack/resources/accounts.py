"""Account resource."""

from __future__ import annotations

from typing import TYPE_CHECKING

from oack.types.accounts import Account, AccountInvite, AccountMember, Subscription

if TYPE_CHECKING:
    from oack._client import AsyncBaseClient, BaseClient


class AsyncAccounts:
    def __init__(self, client: AsyncBaseClient) -> None:
        self._client = client

    async def create(self, name: str) -> Account:
        resp = await self._client.request("POST", "/api/v1/accounts", json={"name": name})
        return Account.model_validate_json(resp)

    async def list(self) -> list[Account]:
        resp = await self._client.request("GET", "/api/v1/accounts")
        return [Account.model_validate(a) for a in _parse_list(resp)]

    async def get(self, account_id: str) -> Account:
        resp = await self._client.request("GET", f"/api/v1/accounts/{account_id}")
        return Account.model_validate_json(resp)

    async def update(self, account_id: str, name: str) -> Account:
        resp = await self._client.request("PUT", f"/api/v1/accounts/{account_id}", json={"name": name})
        return Account.model_validate_json(resp)

    async def delete(self, account_id: str) -> None:
        await self._client.request("DELETE", f"/api/v1/accounts/{account_id}")

    async def restore(self, account_id: str) -> Account:
        resp = await self._client.request("POST", f"/api/v1/accounts/{account_id}/restore")
        return Account.model_validate_json(resp)

    async def transfer(self, account_id: str, user_id: str) -> Account:
        resp = await self._client.request(
            "POST", f"/api/v1/accounts/{account_id}/transfer", json={"user_id": user_id}
        )
        return Account.model_validate_json(resp)

    async def list_members(self, account_id: str) -> list[AccountMember]:
        resp = await self._client.request("GET", f"/api/v1/accounts/{account_id}/members")
        return [AccountMember.model_validate(m) for m in _parse_list(resp)]

    async def set_member_role(self, account_id: str, user_id: str, role: str) -> AccountMember:
        resp = await self._client.request(
            "PUT", f"/api/v1/accounts/{account_id}/members/{user_id}/role", json={"role": role}
        )
        return AccountMember.model_validate_json(resp)

    async def remove_member(self, account_id: str, user_id: str) -> None:
        await self._client.request("DELETE", f"/api/v1/accounts/{account_id}/members/{user_id}")

    async def get_subscription(self, account_id: str) -> Subscription:
        resp = await self._client.request("GET", f"/api/v1/accounts/{account_id}/subscription")
        return Subscription.model_validate_json(resp)

    async def update_subscription(self, account_id: str, plan: str, status: str) -> Subscription:
        resp = await self._client.request(
            "PUT", f"/api/v1/accounts/{account_id}/subscription", json={"plan": plan, "status": status}
        )
        return Subscription.model_validate_json(resp)

    async def create_invite(self, account_id: str, email: str, role: str) -> AccountInvite:
        resp = await self._client.request(
            "POST", f"/api/v1/accounts/{account_id}/invites", json={"email": email, "role": role}
        )
        return AccountInvite.model_validate_json(resp)

    async def list_invites(self, account_id: str) -> list[AccountInvite]:
        resp = await self._client.request("GET", f"/api/v1/accounts/{account_id}/invites")
        return [AccountInvite.model_validate(i) for i in _parse_list(resp)]

    async def revoke_invite(self, account_id: str, invite_id: str) -> None:
        await self._client.request("DELETE", f"/api/v1/accounts/{account_id}/invites/{invite_id}")


class Accounts:
    def __init__(self, client: BaseClient) -> None:
        self._client = client

    def create(self, name: str) -> Account:
        resp = self._client.request("POST", "/api/v1/accounts", json={"name": name})
        return Account.model_validate_json(resp)

    def list(self) -> list[Account]:
        resp = self._client.request("GET", "/api/v1/accounts")
        return [Account.model_validate(a) for a in _parse_list(resp)]

    def get(self, account_id: str) -> Account:
        resp = self._client.request("GET", f"/api/v1/accounts/{account_id}")
        return Account.model_validate_json(resp)

    def update(self, account_id: str, name: str) -> Account:
        resp = self._client.request("PUT", f"/api/v1/accounts/{account_id}", json={"name": name})
        return Account.model_validate_json(resp)

    def delete(self, account_id: str) -> None:
        self._client.request("DELETE", f"/api/v1/accounts/{account_id}")

    def restore(self, account_id: str) -> Account:
        resp = self._client.request("POST", f"/api/v1/accounts/{account_id}/restore")
        return Account.model_validate_json(resp)

    def transfer(self, account_id: str, user_id: str) -> Account:
        resp = self._client.request(
            "POST", f"/api/v1/accounts/{account_id}/transfer", json={"user_id": user_id}
        )
        return Account.model_validate_json(resp)

    def list_members(self, account_id: str) -> list[AccountMember]:
        resp = self._client.request("GET", f"/api/v1/accounts/{account_id}/members")
        return [AccountMember.model_validate(m) for m in _parse_list(resp)]

    def set_member_role(self, account_id: str, user_id: str, role: str) -> AccountMember:
        resp = self._client.request(
            "PUT", f"/api/v1/accounts/{account_id}/members/{user_id}/role", json={"role": role}
        )
        return AccountMember.model_validate_json(resp)

    def remove_member(self, account_id: str, user_id: str) -> None:
        self._client.request("DELETE", f"/api/v1/accounts/{account_id}/members/{user_id}")

    def get_subscription(self, account_id: str) -> Subscription:
        resp = self._client.request("GET", f"/api/v1/accounts/{account_id}/subscription")
        return Subscription.model_validate_json(resp)

    def update_subscription(self, account_id: str, plan: str, status: str) -> Subscription:
        resp = self._client.request(
            "PUT", f"/api/v1/accounts/{account_id}/subscription", json={"plan": plan, "status": status}
        )
        return Subscription.model_validate_json(resp)

    def create_invite(self, account_id: str, email: str, role: str) -> AccountInvite:
        resp = self._client.request(
            "POST", f"/api/v1/accounts/{account_id}/invites", json={"email": email, "role": role}
        )
        return AccountInvite.model_validate_json(resp)

    def list_invites(self, account_id: str) -> list[AccountInvite]:
        resp = self._client.request("GET", f"/api/v1/accounts/{account_id}/invites")
        return [AccountInvite.model_validate(i) for i in _parse_list(resp)]

    def revoke_invite(self, account_id: str, invite_id: str) -> None:
        self._client.request("DELETE", f"/api/v1/accounts/{account_id}/invites/{invite_id}")


def _parse_list(resp: bytes) -> list[dict]:  # type: ignore[type-arg]
    import json
    return json.loads(resp)  # type: ignore[no-any-return]
