"""Acceptance tests — run against a real API (localhost or production).

Requires environment variables:
    OACK_API_KEY     — account-level API key (e.g. oack_acc_...)
    OACK_ACCOUNT_ID  — account UUID
    OACK_API_URL     — API base URL (default: http://localhost:8080)

Run:
    OACK_API_KEY=... OACK_ACCOUNT_ID=... pytest tests/test_acc.py -v
"""

from __future__ import annotations

import os
import time

import pytest

from oack import Oack
from oack.types.monitors import CreateMonitorParams

API_KEY = os.environ.get("OACK_API_KEY", "")
ACCOUNT_ID = os.environ.get("OACK_ACCOUNT_ID", "")
API_URL = os.environ.get("OACK_API_URL", "http://localhost:8080")

pytestmark = pytest.mark.skipif(
    not API_KEY or not ACCOUNT_ID,
    reason="OACK_API_KEY and OACK_ACCOUNT_ID must be set",
)


@pytest.fixture(scope="module")
def client() -> Oack:
    c = Oack(api_key=API_KEY, base_url=API_URL)
    yield c  # type: ignore[misc]
    c.close()


@pytest.fixture(scope="module")
def unique() -> str:
    return str(int(time.time() * 1000))


# ---------------------------------------------------------------------------
# Teams
# ---------------------------------------------------------------------------


class TestTeams:
    def test_lifecycle(self, client: Oack, unique: str) -> None:
        name = f"py-acc-team-{unique}"

        # Create
        team = client.teams.create(ACCOUNT_ID, name)
        assert team.id
        assert team.name == name
        team_id = team.id

        try:
            # Read
            fetched = client.teams.get(team_id)
            assert fetched.id == team_id
            assert fetched.name == name

            # List
            teams = client.teams.list()
            assert any(t.id == team_id for t in teams)

            # Update
            updated = client.teams.update(team_id, f"{name}-updated")
            assert updated.name == f"{name}-updated"

            # Members
            members = client.teams.list_members(team_id)
            assert len(members) >= 1
        finally:
            # Delete
            client.teams.delete(team_id)


# ---------------------------------------------------------------------------
# Monitors
# ---------------------------------------------------------------------------


class TestMonitors:
    @pytest.fixture(autouse=True)
    def _setup(self, client: Oack, unique: str) -> None:
        self.client = client
        self.team = client.teams.create(ACCOUNT_ID, f"py-acc-mon-team-{unique}")
        self.team_id = self.team.id
        yield
        client.teams.delete(self.team_id)

    def test_lifecycle(self, unique: str) -> None:
        name = f"py-acc-monitor-{unique}"

        # Create
        monitor = self.client.monitors.create(
            self.team_id,
            CreateMonitorParams(name=name, url="https://example.com"),
        )
        assert monitor.id
        assert monitor.name == name
        assert monitor.url == "https://example.com"
        monitor_id = monitor.id

        # Read
        fetched = self.client.monitors.get(self.team_id, monitor_id)
        assert fetched.id == monitor_id

        # List
        monitors = self.client.monitors.list(self.team_id)
        assert any(m.id == monitor_id for m in monitors)

        # Update
        updated = self.client.monitors.update(
            self.team_id,
            monitor_id,
            CreateMonitorParams(name=f"{name}-updated", url="https://example.com"),
        )
        assert updated.name == f"{name}-updated"

        # Pause / Unpause
        paused = self.client.monitors.pause(self.team_id, monitor_id)
        assert paused.status == "paused"

        unpaused = self.client.monitors.unpause(self.team_id, monitor_id)
        assert unpaused.status == "active"

        # Duplicate
        dup = self.client.monitors.duplicate(self.team_id, monitor_id)
        assert dup.id != monitor_id
        assert dup.url == "https://example.com"
        self.client.monitors.delete(self.team_id, dup.id)

        # Delete
        self.client.monitors.delete(self.team_id, monitor_id)


# ---------------------------------------------------------------------------
# Alert Channels
# ---------------------------------------------------------------------------


class TestAlertChannels:
    @pytest.fixture(autouse=True)
    def _setup(self, client: Oack, unique: str) -> None:
        self.client = client
        self.team = client.teams.create(ACCOUNT_ID, f"py-acc-alert-team-{unique}")
        self.team_id = self.team.id
        yield
        client.teams.delete(self.team_id)

    def test_lifecycle(self, unique: str) -> None:
        from oack.types.alert_channels import CreateAlertChannelParams

        name = f"py-acc-webhook-{unique}"

        # Create
        ch = self.client.alert_channels.create(
            self.team_id,
            CreateAlertChannelParams(
                type="webhook",
                name=name,
                config={"url": "https://httpbin.org/post"},
            ),
        )
        assert ch.id
        assert ch.type == "webhook"
        channel_id = ch.id

        # List
        channels = self.client.alert_channels.list(self.team_id)
        assert any(c.id == channel_id for c in channels)

        # Get (via list + find)
        fetched = self.client.alert_channels.get(self.team_id, channel_id)
        assert fetched.name == name

        # Delete
        self.client.alert_channels.delete(self.team_id, channel_id)


# ---------------------------------------------------------------------------
# Accounts
# ---------------------------------------------------------------------------


class TestAccounts:
    def test_read(self, client: Oack) -> None:
        # List
        accounts = client.accounts.list()
        assert len(accounts) >= 1

        # Get
        account = client.accounts.get(ACCOUNT_ID)
        assert account.id == ACCOUNT_ID

        # Members
        members = client.accounts.list_members(ACCOUNT_ID)
        assert len(members) >= 1

        # Subscription
        sub = client.accounts.get_subscription(ACCOUNT_ID)
        assert sub.account_id == ACCOUNT_ID


# ---------------------------------------------------------------------------
# Metrics & Probes (read-only, needs an existing monitor with probes)
# ---------------------------------------------------------------------------


class TestMetrics:
    @pytest.fixture(autouse=True)
    def _setup(self, client: Oack, unique: str) -> None:
        self.client = client
        self.team = client.teams.create(ACCOUNT_ID, f"py-acc-metrics-team-{unique}")
        self.team_id = self.team.id
        self.monitor = client.monitors.create(
            self.team_id,
            CreateMonitorParams(name=f"py-acc-metrics-mon-{unique}", url="https://example.com"),
        )
        self.monitor_id = self.monitor.id
        yield
        client.monitors.delete(self.team_id, self.monitor_id)
        client.teams.delete(self.team_id)

    def test_monitor_metrics(self) -> None:
        metrics = self.client.metrics.get_monitor_metrics(self.team_id, self.monitor_id)
        assert metrics.last_24h is not None

    def test_expiration(self) -> None:
        exp = self.client.metrics.get_expiration(self.team_id, self.monitor_id)
        assert exp is not None

    def test_probes_list(self) -> None:
        probes = self.client.probes.list(self.team_id, self.monitor_id)
        assert probes.total >= 0


# ---------------------------------------------------------------------------
# Geo
# ---------------------------------------------------------------------------


class TestGeo:
    def test_list_regions(self, client: Oack) -> None:
        regions = client.geo.list_regions()
        assert isinstance(regions, list)

    def test_list_checkers(self, client: Oack) -> None:
        checkers = client.geo.list_checkers()
        assert isinstance(checkers, list)


# ---------------------------------------------------------------------------
# External Links
# ---------------------------------------------------------------------------


class TestExternalLinks:
    @pytest.fixture(autouse=True)
    def _setup(self, client: Oack, unique: str) -> None:
        self.client = client
        self.team = client.teams.create(ACCOUNT_ID, f"py-acc-extlink-team-{unique}")
        self.team_id = self.team.id
        yield
        client.teams.delete(self.team_id)

    def test_lifecycle(self, unique: str) -> None:
        name = f"py-acc-link-{unique}"

        link = self.client.external_links.create(
            self.team_id,
            {"name": name, "url_template": "https://grafana.example.com/d/abc?from={{from}}&to={{to}}", "time_window_minutes": 30},
        )
        assert link.id
        link_id = link.id

        links = self.client.external_links.list(self.team_id)
        assert any(el.id == link_id for el in links)

        fetched = self.client.external_links.get(self.team_id, link_id)
        assert fetched.name == name

        self.client.external_links.delete(self.team_id, link_id)


# ---------------------------------------------------------------------------
# User (whoami)
# ---------------------------------------------------------------------------


class TestUser:
    def test_whoami(self, client: Oack) -> None:
        user = client.user.whoami()
        assert user.id
