"""Oack — Official Python client for the Oack monitoring API."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from collections.abc import Callable

from oack._auth import async_device_flow_authenticate, device_flow_authenticate
from oack._client import AsyncBaseClient, BaseClient
from oack._exceptions import (
    APIError,
    AuthenticationError,
    ConflictError,
    ForbiddenError,
    NotFoundError,
    OackError,
    RateLimitError,
)
from oack.resources.accounts import Accounts, AsyncAccounts
from oack.resources.alert_channels import AlertChannels, AsyncAlertChannels
from oack.resources.browser_probes import AsyncBrowserProbes, BrowserProbes
from oack.resources.cf_logs import AsyncCFLogs, CFLogs
from oack.resources.comments import AsyncComments, Comments
from oack.resources.external_links import AsyncExternalLinks, ExternalLinks
from oack.resources.geo import AsyncGeo, Geo
from oack.resources.integrations import AsyncIntegrations, Integrations
from oack.resources.metrics import AsyncMetrics, Metrics
from oack.resources.monitors import AsyncMonitors, Monitors
from oack.resources.notifications import AsyncNotifications, Notifications
from oack.resources.probes import AsyncProbes, Probes
from oack.resources.shares import AsyncShares, Shares
from oack.resources.status_pages import AsyncStatusPages, StatusPages
from oack.resources.teams import AsyncTeams, Teams
from oack.resources.traces import AsyncTraces, Traces
from oack.resources.user import AsyncUser, SyncUser
from oack.resources.watchdogs import AsyncWatchdogs, Watchdogs

__version__ = "0.1.0"


class AsyncOack:
    """Async Oack API client.

    Usage::

        async with AsyncOack(api_key="sk-...") as client:
            teams = await client.teams.list()
    """

    def __init__(
        self,
        *,
        api_key: str | None = None,
        api_key_func: Callable[[], str] | None = None,
        base_url: str = "https://api.oack.io",
        timeout: float = 30.0,
        max_retries: int = 2,
    ) -> None:
        self._client = AsyncBaseClient(
            api_key=api_key,
            api_key_func=api_key_func,
            base_url=base_url,
            timeout=timeout,
            max_retries=max_retries,
        )
        self.accounts = AsyncAccounts(self._client)
        self.teams = AsyncTeams(self._client)
        self.monitors = AsyncMonitors(self._client)
        self.probes = AsyncProbes(self._client)
        self.alert_channels = AsyncAlertChannels(self._client)
        self.metrics = AsyncMetrics(self._client)
        self.geo = AsyncGeo(self._client)
        self.status_pages = AsyncStatusPages(self._client)
        self.comments = AsyncComments(self._client)
        self.external_links = AsyncExternalLinks(self._client)
        self.integrations = AsyncIntegrations(self._client)
        self.notifications = AsyncNotifications(self._client)
        self.shares = AsyncShares(self._client)
        self.traces = AsyncTraces(self._client)
        self.user = AsyncUser(self._client)
        self.cf_logs = AsyncCFLogs(self._client)
        self.browser_probes = AsyncBrowserProbes(self._client)
        self.watchdogs = AsyncWatchdogs(self._client)

    async def close(self) -> None:
        await self._client.close()

    async def __aenter__(self) -> AsyncOack:
        return self

    async def __aexit__(self, *args: Any) -> None:
        await self.close()


class Oack:
    """Sync Oack API client.

    Usage::

        with Oack(api_key="sk-...") as client:
            teams = client.teams.list()
    """

    def __init__(
        self,
        *,
        api_key: str | None = None,
        api_key_func: Callable[[], str] | None = None,
        base_url: str = "https://api.oack.io",
        timeout: float = 30.0,
        max_retries: int = 2,
    ) -> None:
        self._client = BaseClient(
            api_key=api_key,
            api_key_func=api_key_func,
            base_url=base_url,
            timeout=timeout,
            max_retries=max_retries,
        )
        self.accounts = Accounts(self._client)
        self.teams = Teams(self._client)
        self.monitors = Monitors(self._client)
        self.probes = Probes(self._client)
        self.alert_channels = AlertChannels(self._client)
        self.metrics = Metrics(self._client)
        self.geo = Geo(self._client)
        self.status_pages = StatusPages(self._client)
        self.comments = Comments(self._client)
        self.external_links = ExternalLinks(self._client)
        self.integrations = Integrations(self._client)
        self.notifications = Notifications(self._client)
        self.shares = Shares(self._client)
        self.traces = Traces(self._client)
        self.user = SyncUser(self._client)
        self.cf_logs = CFLogs(self._client)
        self.browser_probes = BrowserProbes(self._client)
        self.watchdogs = Watchdogs(self._client)

    def close(self) -> None:
        self._client.close()

    def __enter__(self) -> Oack:
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()


__all__ = [
    "APIError",
    "AsyncOack",
    "AuthenticationError",
    "ConflictError",
    "ForbiddenError",
    "NotFoundError",
    "Oack",
    "OackError",
    "RateLimitError",
    "__version__",
    "async_device_flow_authenticate",
    "device_flow_authenticate",
]
