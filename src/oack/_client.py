"""Base HTTP client with auth, retry, and error handling."""

from __future__ import annotations

import random
import time
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from collections.abc import Callable

import httpx

from oack._exceptions import _parse_error

_DEFAULT_BASE_URL = "https://api.oack.io"
_DEFAULT_TIMEOUT = 30.0
_DEFAULT_MAX_RETRIES = 2
_RETRYABLE_STATUS_CODES = {408, 429, 500, 502, 503, 504}
_IDEMPOTENT_METHODS = {"GET", "PUT", "DELETE", "HEAD", "OPTIONS"}


class AsyncBaseClient:
    """Async HTTP client for the Oack API."""

    def __init__(
        self,
        *,
        api_key: str | None = None,
        api_key_func: Callable[[], str] | None = None,
        base_url: str = _DEFAULT_BASE_URL,
        timeout: float = _DEFAULT_TIMEOUT,
        max_retries: int = _DEFAULT_MAX_RETRIES,
        http_client: httpx.AsyncClient | None = None,
    ) -> None:
        if api_key is None and api_key_func is None:
            msg = "either api_key or api_key_func is required"
            raise ValueError(msg)
        self._api_key = api_key
        self._api_key_func = api_key_func
        self._base_url = base_url.rstrip("/")
        self._max_retries = max_retries
        self._owns_client = http_client is None
        self._client = http_client or httpx.AsyncClient(timeout=timeout)

    def _token(self) -> str:
        if self._api_key_func is not None:
            return self._api_key_func()
        return self._api_key or ""

    async def request(
        self,
        method: str,
        path: str,
        *,
        json: Any = None,
        params: dict[str, str] | None = None,
    ) -> bytes:
        url = self._base_url + path
        headers: dict[str, str] = {}
        token = self._token()
        if token:
            headers["Authorization"] = f"Bearer {token}"
        if json is not None:
            headers["Content-Type"] = "application/json"

        last_exc: Exception | None = None
        for attempt in range(1 + self._max_retries):
            try:
                resp = await self._client.request(
                    method,
                    url,
                    json=json,
                    params=params,
                    headers=headers,
                )
            except httpx.TransportError as exc:
                last_exc = exc
                if attempt < self._max_retries and method.upper() in _IDEMPOTENT_METHODS:
                    await self._backoff(attempt)
                    continue
                raise

            if resp.status_code < 400:
                return resp.content

            retry_after = self._parse_retry_after(resp)
            if (
                resp.status_code in _RETRYABLE_STATUS_CODES
                and attempt < self._max_retries
                and (method.upper() in _IDEMPOTENT_METHODS or resp.status_code == 429)
            ):
                delay = retry_after if retry_after and retry_after > 0 else self._backoff_delay(attempt)
                import asyncio

                await asyncio.sleep(delay)
                continue

            raise _parse_error(resp.status_code, resp.content, retry_after=retry_after)

        if last_exc is not None:
            raise last_exc
        msg = "max retries exceeded"
        raise RuntimeError(msg)

    @staticmethod
    def _parse_retry_after(resp: httpx.Response) -> float | None:
        val = resp.headers.get("retry-after")
        if val is None:
            return None
        try:
            return float(val)
        except ValueError:
            return None

    @staticmethod
    def _backoff_delay(attempt: int) -> float:
        return min(0.5 * (2**attempt) + random.uniform(0, 0.25), 30.0)  # noqa: S311

    @staticmethod
    async def _backoff(attempt: int) -> None:
        import asyncio

        delay = min(0.5 * (2**attempt) + random.uniform(0, 0.25), 30.0)  # noqa: S311
        await asyncio.sleep(delay)

    async def close(self) -> None:
        if self._owns_client:
            await self._client.aclose()

    async def __aenter__(self) -> AsyncBaseClient:
        return self

    async def __aexit__(self, *args: Any) -> None:
        await self.close()


class BaseClient:
    """Sync HTTP client for the Oack API."""

    def __init__(
        self,
        *,
        api_key: str | None = None,
        api_key_func: Callable[[], str] | None = None,
        base_url: str = _DEFAULT_BASE_URL,
        timeout: float = _DEFAULT_TIMEOUT,
        max_retries: int = _DEFAULT_MAX_RETRIES,
        http_client: httpx.Client | None = None,
    ) -> None:
        if api_key is None and api_key_func is None:
            msg = "either api_key or api_key_func is required"
            raise ValueError(msg)
        self._api_key = api_key
        self._api_key_func = api_key_func
        self._base_url = base_url.rstrip("/")
        self._max_retries = max_retries
        self._owns_client = http_client is None
        self._client = http_client or httpx.Client(timeout=timeout)

    def _token(self) -> str:
        if self._api_key_func is not None:
            return self._api_key_func()
        return self._api_key or ""

    def request(
        self,
        method: str,
        path: str,
        *,
        json: Any = None,
        params: dict[str, str] | None = None,
    ) -> bytes:
        url = self._base_url + path
        headers: dict[str, str] = {}
        token = self._token()
        if token:
            headers["Authorization"] = f"Bearer {token}"
        if json is not None:
            headers["Content-Type"] = "application/json"

        last_exc: Exception | None = None
        for attempt in range(1 + self._max_retries):
            try:
                resp = self._client.request(
                    method,
                    url,
                    json=json,
                    params=params,
                    headers=headers,
                )
            except httpx.TransportError as exc:
                last_exc = exc
                if attempt < self._max_retries and method.upper() in _IDEMPOTENT_METHODS:
                    delay = self._backoff_delay(attempt)
                    time.sleep(delay)
                    continue
                raise

            if resp.status_code < 400:
                return resp.content

            retry_after = self._parse_retry_after(resp)
            if (
                resp.status_code in _RETRYABLE_STATUS_CODES
                and attempt < self._max_retries
                and (method.upper() in _IDEMPOTENT_METHODS or resp.status_code == 429)
            ):
                delay = retry_after if retry_after and retry_after > 0 else self._backoff_delay(attempt)
                time.sleep(delay)
                continue

            raise _parse_error(resp.status_code, resp.content, retry_after=retry_after)

        if last_exc is not None:
            raise last_exc
        msg = "max retries exceeded"
        raise RuntimeError(msg)

    @staticmethod
    def _parse_retry_after(resp: httpx.Response) -> float | None:
        val = resp.headers.get("retry-after")
        if val is None:
            return None
        try:
            return float(val)
        except ValueError:
            return None

    @staticmethod
    def _backoff_delay(attempt: int) -> float:
        return min(0.5 * (2**attempt) + random.uniform(0, 0.25), 30.0)  # noqa: S311

    def close(self) -> None:
        if self._owns_client:
            self._client.close()

    def __enter__(self) -> BaseClient:
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()
