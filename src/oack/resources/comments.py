"""Comment resource."""

from __future__ import annotations

import json
from typing import TYPE_CHECKING

from oack.types.comments import Comment, CommentEdit

if TYPE_CHECKING:
    from oack._client import AsyncBaseClient, BaseClient


def _comment_path(team_id: str, monitor_id: str) -> str:
    return f"/api/v1/teams/{team_id}/monitors/{monitor_id}/comments"


class AsyncComments:
    def __init__(self, client: AsyncBaseClient) -> None:
        self._client = client

    async def create(self, team_id: str, monitor_id: str, body: str) -> Comment:
        resp = await self._client.request("POST", _comment_path(team_id, monitor_id), json={"body": body})
        return Comment.model_validate_json(resp)

    async def list(self, team_id: str, monitor_id: str) -> list[Comment]:
        resp = await self._client.request("GET", _comment_path(team_id, monitor_id))
        return [Comment.model_validate(c) for c in json.loads(resp)]

    async def edit(self, team_id: str, monitor_id: str, comment_id: str, body: str) -> Comment:
        resp = await self._client.request(
            "PUT", _comment_path(team_id, monitor_id) + f"/{comment_id}", json={"body": body}
        )
        return Comment.model_validate_json(resp)

    async def delete(self, team_id: str, monitor_id: str, comment_id: str) -> None:
        await self._client.request("DELETE", _comment_path(team_id, monitor_id) + f"/{comment_id}")

    async def reply(self, team_id: str, monitor_id: str, comment_id: str, body: str) -> Comment:
        resp = await self._client.request(
            "POST",
            _comment_path(team_id, monitor_id) + f"/{comment_id}/replies",
            json={"body": body},
        )
        return Comment.model_validate_json(resp)

    async def list_replies(self, team_id: str, monitor_id: str, comment_id: str) -> list[Comment]:
        resp = await self._client.request("GET", _comment_path(team_id, monitor_id) + f"/{comment_id}/replies")
        return [Comment.model_validate(c) for c in json.loads(resp)]

    async def resolve(self, team_id: str, monitor_id: str, comment_id: str) -> Comment:
        resp = await self._client.request("POST", _comment_path(team_id, monitor_id) + f"/{comment_id}/resolve")
        return Comment.model_validate_json(resp)

    async def reopen(self, team_id: str, monitor_id: str, comment_id: str) -> Comment:
        resp = await self._client.request("POST", _comment_path(team_id, monitor_id) + f"/{comment_id}/reopen")
        return Comment.model_validate_json(resp)

    async def list_edits(self, team_id: str, monitor_id: str, comment_id: str) -> list[CommentEdit]:
        resp = await self._client.request("GET", _comment_path(team_id, monitor_id) + f"/{comment_id}/edits")
        return [CommentEdit.model_validate(e) for e in json.loads(resp)]

    async def list_by_team(self, team_id: str) -> list[Comment]:
        resp = await self._client.request("GET", f"/api/v1/teams/{team_id}/comments")
        return [Comment.model_validate(c) for c in json.loads(resp)]

    async def list_by_account(self, account_id: str) -> list[Comment]:
        resp = await self._client.request("GET", f"/api/v1/accounts/{account_id}/comments")
        return [Comment.model_validate(c) for c in json.loads(resp)]


class Comments:
    def __init__(self, client: BaseClient) -> None:
        self._client = client

    def create(self, team_id: str, monitor_id: str, body: str) -> Comment:
        resp = self._client.request("POST", _comment_path(team_id, monitor_id), json={"body": body})
        return Comment.model_validate_json(resp)

    def list(self, team_id: str, monitor_id: str) -> list[Comment]:
        resp = self._client.request("GET", _comment_path(team_id, monitor_id))
        return [Comment.model_validate(c) for c in json.loads(resp)]

    def edit(self, team_id: str, monitor_id: str, comment_id: str, body: str) -> Comment:
        resp = self._client.request("PUT", _comment_path(team_id, monitor_id) + f"/{comment_id}", json={"body": body})
        return Comment.model_validate_json(resp)

    def delete(self, team_id: str, monitor_id: str, comment_id: str) -> None:
        self._client.request("DELETE", _comment_path(team_id, monitor_id) + f"/{comment_id}")

    def reply(self, team_id: str, monitor_id: str, comment_id: str, body: str) -> Comment:
        resp = self._client.request(
            "POST",
            _comment_path(team_id, monitor_id) + f"/{comment_id}/replies",
            json={"body": body},
        )
        return Comment.model_validate_json(resp)

    def list_replies(self, team_id: str, monitor_id: str, comment_id: str) -> list[Comment]:
        resp = self._client.request("GET", _comment_path(team_id, monitor_id) + f"/{comment_id}/replies")
        return [Comment.model_validate(c) for c in json.loads(resp)]

    def resolve(self, team_id: str, monitor_id: str, comment_id: str) -> Comment:
        resp = self._client.request("POST", _comment_path(team_id, monitor_id) + f"/{comment_id}/resolve")
        return Comment.model_validate_json(resp)

    def reopen(self, team_id: str, monitor_id: str, comment_id: str) -> Comment:
        resp = self._client.request("POST", _comment_path(team_id, monitor_id) + f"/{comment_id}/reopen")
        return Comment.model_validate_json(resp)

    def list_edits(self, team_id: str, monitor_id: str, comment_id: str) -> list[CommentEdit]:
        resp = self._client.request("GET", _comment_path(team_id, monitor_id) + f"/{comment_id}/edits")
        return [CommentEdit.model_validate(e) for e in json.loads(resp)]

    def list_by_team(self, team_id: str) -> list[Comment]:
        resp = self._client.request("GET", f"/api/v1/teams/{team_id}/comments")
        return [Comment.model_validate(c) for c in json.loads(resp)]

    def list_by_account(self, account_id: str) -> list[Comment]:
        resp = self._client.request("GET", f"/api/v1/accounts/{account_id}/comments")
        return [Comment.model_validate(c) for c in json.loads(resp)]
