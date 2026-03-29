"""Test script resource."""

from __future__ import annotations

import json
import time
from typing import TYPE_CHECKING

from oack.types.test_script import TestScriptParams, TestScriptResult

if TYPE_CHECKING:
    from oack._client import AsyncBaseClient, BaseClient

_POLL_INTERVAL = 2  # seconds
_TIMEOUT = 300  # 5 minutes


def _test_script_path(team_id: str, monitor_id: str) -> str:
    return f"/api/v1/teams/{team_id}/monitors/{monitor_id}/test-script"


class AsyncTestScript:
    def __init__(self, client: AsyncBaseClient) -> None:
        self._client = client

    async def run(self, team_id: str, monitor_id: str, params: TestScriptParams) -> TestScriptResult:
        import asyncio

        submit_path = _test_script_path(team_id, monitor_id)
        resp = await self._client.request("POST", submit_path, json=params.model_dump(exclude_none=True))
        submit = json.loads(resp)
        test_id = submit.get("test_id")
        if not test_id:
            msg = "server returned empty test_id"
            raise ValueError(msg)

        poll_path = f"{submit_path}/{test_id}"
        deadline = time.monotonic() + _TIMEOUT

        while time.monotonic() < deadline:
            await asyncio.sleep(_POLL_INTERVAL)
            resp = await self._client.request("GET", poll_path)
            poll = json.loads(resp)
            if poll.get("status") == "done" and poll.get("result"):
                return TestScriptResult.model_validate(poll["result"])

        msg = f"test timed out after {_TIMEOUT}s"
        raise TimeoutError(msg)


class TestScript:
    def __init__(self, client: BaseClient) -> None:
        self._client = client

    def run(self, team_id: str, monitor_id: str, params: TestScriptParams) -> TestScriptResult:
        submit_path = _test_script_path(team_id, monitor_id)
        resp = self._client.request("POST", submit_path, json=params.model_dump(exclude_none=True))
        submit = json.loads(resp)
        test_id = submit.get("test_id")
        if not test_id:
            msg = "server returned empty test_id"
            raise ValueError(msg)

        poll_path = f"{submit_path}/{test_id}"
        deadline = time.monotonic() + _TIMEOUT

        while time.monotonic() < deadline:
            time.sleep(_POLL_INTERVAL)
            resp = self._client.request("GET", poll_path)
            poll = json.loads(resp)
            if poll.get("status") == "done" and poll.get("result"):
                return TestScriptResult.model_validate(poll["result"])

        msg = f"test timed out after {_TIMEOUT}s"
        raise TimeoutError(msg)
