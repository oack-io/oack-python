"""RFC 8628 Device Authorization Flow — browser-based login with in-memory JWT."""

from __future__ import annotations

import time
import webbrowser

import httpx

_DEFAULT_BASE_URL = "https://api.oack.io"


def device_flow_authenticate(
    base_url: str = _DEFAULT_BASE_URL,
    *,
    timeout: float = 30.0,
    open_browser: bool = True,
) -> str:
    """Run the RFC 8628 device authorization flow and return a JWT.

    Opens the verification URL in the default browser, then polls until
    the user completes authentication. The token is returned as a plain
    string and lives only in memory — it is never written to disk.

    Args:
        base_url: API base URL (default: https://api.oack.io).
        timeout: HTTP request timeout in seconds.
        open_browser: Whether to auto-open the verification URL.

    Returns:
        The signed JWT access token.

    Raises:
        OackError: If the flow fails or the device code expires.
    """
    from oack._exceptions import OackError

    client = httpx.Client(timeout=timeout)
    try:
        resp = client.post(f"{base_url}/api/v1/auth/device/code")
        if resp.status_code != 200:
            raise OackError(f"device code request failed: HTTP {resp.status_code}")

        data = resp.json()
        device_code: str = data["device_code"]
        user_code: str = data["user_code"]
        verification_url: str = data["verification_uri_complete"]
        interval: int = data.get("interval", 5)

        print("\nTo authenticate, open the following URL in your browser:\n")  # noqa: T201
        print(f"  {verification_url}\n")  # noqa: T201
        print(f"User code: {user_code}\n")  # noqa: T201
        print("Waiting for authorization...\n")  # noqa: T201

        if open_browser:
            webbrowser.open(verification_url)

        poll_interval = interval
        while True:
            time.sleep(poll_interval)
            token_resp = client.post(
                f"{base_url}/api/v1/auth/device/token",
                data={"device_code": device_code},
            )
            token_data = token_resp.json()
            error = token_data.get("error", "")

            if not error:
                print("Authenticated successfully.\n")  # noqa: T201
                return token_data["access_token"]

            if error == "authorization_pending":
                continue
            if error == "slow_down":
                poll_interval += 5
                continue
            if error == "expired_token":
                raise OackError("device code expired — re-run to start a new flow")

            raise OackError(f"unexpected token endpoint error: {error}")
    finally:
        client.close()


async def async_device_flow_authenticate(
    base_url: str = _DEFAULT_BASE_URL,
    *,
    timeout: float = 30.0,
    open_browser: bool = True,
) -> str:
    """Async version of :func:`device_flow_authenticate`.

    Same behavior — opens browser, polls for token, returns JWT in memory.
    """
    import asyncio

    from oack._exceptions import OackError

    async with httpx.AsyncClient(timeout=timeout) as client:
        resp = await client.post(f"{base_url}/api/v1/auth/device/code")
        if resp.status_code != 200:
            raise OackError(f"device code request failed: HTTP {resp.status_code}")

        data = resp.json()
        device_code: str = data["device_code"]
        user_code: str = data["user_code"]
        verification_url: str = data["verification_uri_complete"]
        interval: int = data.get("interval", 5)

        print("\nTo authenticate, open the following URL in your browser:\n")  # noqa: T201
        print(f"  {verification_url}\n")  # noqa: T201
        print(f"User code: {user_code}\n")  # noqa: T201
        print("Waiting for authorization...\n")  # noqa: T201

        if open_browser:
            webbrowser.open(verification_url)

        poll_interval = interval
        while True:
            await asyncio.sleep(poll_interval)
            token_resp = await client.post(
                f"{base_url}/api/v1/auth/device/token",
                data={"device_code": device_code},
            )
            token_data = token_resp.json()
            error = token_data.get("error", "")

            if not error:
                print("Authenticated successfully.\n")  # noqa: T201
                return token_data["access_token"]

            if error == "authorization_pending":
                continue
            if error == "slow_down":
                poll_interval += 5
                continue
            if error == "expired_token":
                raise OackError("device code expired — re-run to start a new flow")

            raise OackError(f"unexpected token endpoint error: {error}")
