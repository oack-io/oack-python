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
# Monitor ↔ Alert Channel Linking
# ---------------------------------------------------------------------------


class TestMonitorAlertChannelLink:
    @pytest.fixture(autouse=True)
    def _setup(self, client: Oack, unique: str) -> None:
        self.client = client
        self.team = client.teams.create(ACCOUNT_ID, f"py-acc-link-team-{unique}")
        self.team_id = self.team.id
        self.monitor = client.monitors.create(
            self.team_id,
            CreateMonitorParams(name=f"py-acc-link-mon-{unique}", url="https://example.com"),
        )
        self.monitor_id = self.monitor.id
        from oack.types.alert_channels import CreateAlertChannelParams

        self.channel = client.alert_channels.create(
            self.team_id,
            CreateAlertChannelParams(type="webhook", name=f"py-acc-link-ch-{unique}", config={"url": "https://httpbin.org/post"}),
        )
        self.channel_id = self.channel.id
        yield
        client.monitors.delete(self.team_id, self.monitor_id)
        client.alert_channels.delete(self.team_id, self.channel_id)
        client.teams.delete(self.team_id)

    def test_link_unlink(self) -> None:
        # Link
        self.client.alert_channels.link_monitor_channel(self.team_id, self.monitor_id, self.channel_id)

        # List linked channels
        linked = self.client.alert_channels.list_monitor_channels(self.team_id, self.monitor_id)
        assert self.channel_id in linked

        # Unlink
        self.client.alert_channels.unlink_monitor_channel(self.team_id, self.monitor_id, self.channel_id)

        linked_after = self.client.alert_channels.list_monitor_channels(self.team_id, self.monitor_id)
        assert self.channel_id not in linked_after

    def test_set_monitor_channels(self) -> None:
        result = self.client.alert_channels.set_monitor_channels(self.team_id, self.monitor_id, [self.channel_id])
        assert self.channel_id in result

        # Clear
        cleared = self.client.alert_channels.set_monitor_channels(self.team_id, self.monitor_id, [])
        assert len(cleared) == 0


# ---------------------------------------------------------------------------
# Status Pages (CRUD + Components + Groups + Incidents + Maintenance)
# ---------------------------------------------------------------------------


class TestStatusPages:
    @pytest.fixture(autouse=True)
    def _setup(self, client: Oack, unique: str) -> None:
        self.client = client
        self.unique = unique
        # Need a team + monitor for watchdog
        self.team = client.teams.create(ACCOUNT_ID, f"py-acc-sp-team-{unique}")
        self.team_id = self.team.id
        self.monitor = client.monitors.create(
            self.team_id,
            CreateMonitorParams(name=f"py-acc-sp-mon-{unique}", url="https://example.com"),
        )
        self.monitor_id = self.monitor.id
        yield
        client.monitors.delete(self.team_id, self.monitor_id)
        client.teams.delete(self.team_id)

    def test_full_lifecycle(self) -> None:
        u = self.unique

        # --- Status Page ---
        page = self.client.status_pages.create(
            ACCOUNT_ID,
            {"name": f"py-acc-page-{u}", "slug": f"py-acc-{u}"},
        )
        assert page.id
        assert page.slug == f"py-acc-{u}"
        page_id = page.id

        try:
            fetched = self.client.status_pages.get(ACCOUNT_ID, page_id)
            assert fetched.id == page_id

            pages = self.client.status_pages.list(ACCOUNT_ID)
            assert any(p.id == page_id for p in pages)

            updated = self.client.status_pages.update(
                ACCOUNT_ID, page_id,
                {"name": f"py-acc-page-{u}-updated", "slug": f"py-acc-{u}"},
            )
            assert updated.name == f"py-acc-page-{u}-updated"

            # --- Component Group ---
            group = self.client.status_pages.create_component_group(
                ACCOUNT_ID, page_id,
                {"name": f"py-acc-group-{u}", "position": 0},
            )
            assert group.id
            group_id = group.id

            groups = self.client.status_pages.list_component_groups(ACCOUNT_ID, page_id)
            assert any(g.id == group_id for g in groups)

            # --- Component ---
            comp = self.client.status_pages.create_component(
                ACCOUNT_ID, page_id,
                {"name": f"py-acc-comp-{u}", "position": 0, "group_id": group_id},
            )
            assert comp.id
            comp_id = comp.id

            comps = self.client.status_pages.list_components(ACCOUNT_ID, page_id)
            assert any(c.id == comp_id for c in comps)

            # --- Watchdog ---
            watchdog = self.client.status_pages.create_watchdog(
                ACCOUNT_ID, page_id, comp_id,
                {"monitor_id": self.monitor_id, "severity": "major"},
            )
            assert watchdog.id
            watchdog_id = watchdog.id

            watchdogs = self.client.status_pages.list_watchdogs(ACCOUNT_ID, page_id, comp_id)
            assert any(w.id == watchdog_id for w in watchdogs)

            self.client.status_pages.delete_watchdog(ACCOUNT_ID, page_id, comp_id, watchdog_id)

            # --- Incident ---
            incident = self.client.status_pages.create_incident(
                ACCOUNT_ID, page_id,
                {"title": f"py-acc-incident-{u}", "message": "Test incident", "severity": "minor"},
            )
            assert incident.id
            incident_id = incident.id

            incidents = self.client.status_pages.list_incidents(ACCOUNT_ID, page_id)
            assert any(i.id == incident_id for i in incidents)

            fetched_inc = self.client.status_pages.get_incident(ACCOUNT_ID, page_id, incident_id)
            assert fetched_inc.title == f"py-acc-incident-{u}"

            self.client.status_pages.delete_incident(ACCOUNT_ID, page_id, incident_id)

            # --- Maintenance ---
            maint = self.client.status_pages.create_maintenance(
                ACCOUNT_ID, page_id,
                {"title": f"py-acc-maint-{u}", "message": "Test maintenance", "scheduled_at": "2099-01-01T00:00:00Z"},
            )
            assert maint.id
            maint_id = maint.id

            maints = self.client.status_pages.list_maintenances(ACCOUNT_ID, page_id)
            assert any(m.id == maint_id for m in maints)

            self.client.status_pages.delete_maintenance(ACCOUNT_ID, page_id, maint_id)

            # --- Incident Template ---
            tmpl = self.client.status_pages.create_incident_template(
                ACCOUNT_ID, page_id,
                {"name": f"py-acc-tmpl-{u}", "message": "Template body", "severity": "minor"},
            )
            assert tmpl.id
            tmpl_id = tmpl.id

            tmpls = self.client.status_pages.list_incident_templates(ACCOUNT_ID, page_id)
            assert any(t.id == tmpl_id for t in tmpls)

            self.client.status_pages.delete_incident_template(ACCOUNT_ID, page_id, tmpl_id)

            # Cleanup nested
            self.client.status_pages.delete_component(ACCOUNT_ID, page_id, comp_id)
            self.client.status_pages.delete_component_group(ACCOUNT_ID, page_id, group_id)
        finally:
            self.client.status_pages.delete(ACCOUNT_ID, page_id)


# ---------------------------------------------------------------------------
# Team API Keys
# ---------------------------------------------------------------------------


class TestTeamAPIKeys:
    @pytest.fixture(autouse=True)
    def _setup(self, client: Oack, unique: str) -> None:
        self.client = client
        self.team = client.teams.create(ACCOUNT_ID, f"py-acc-apikey-team-{unique}")
        self.team_id = self.team.id
        yield
        client.teams.delete(self.team_id)

    def test_lifecycle(self, unique: str) -> None:
        # Create
        result = self.client.teams.create_api_key(self.team_id, f"py-acc-key-{unique}")
        assert result.key
        assert result.api_key.id
        key_id = result.api_key.id

        # List
        keys = self.client.teams.list_api_keys(self.team_id)
        assert any(k.id == key_id for k in keys)

        # Delete
        self.client.teams.delete_api_key(self.team_id, key_id)


# ---------------------------------------------------------------------------
# Monitor (full fields)
# ---------------------------------------------------------------------------


class TestMonitorFullFields:
    @pytest.fixture(autouse=True)
    def _setup(self, client: Oack, unique: str) -> None:
        self.client = client
        self.team = client.teams.create(ACCOUNT_ID, f"py-acc-monfull-team-{unique}")
        self.team_id = self.team.id
        yield
        client.teams.delete(self.team_id)

    def test_create_with_all_fields(self, unique: str) -> None:
        monitor = self.client.monitors.create(
            self.team_id,
            CreateMonitorParams(
                name=f"py-acc-full-{unique}",
                url="https://example.com/health",
                check_interval_ms=60000,
                timeout_ms=10000,
                http_method="GET",
                http_version="1.1",
                headers={"X-Test": "true"},
                follow_redirects=True,
                allowed_status_codes=["2xx"],
                failure_threshold=5,
                latency_threshold_ms=5000,
                ssl_expiry_enabled=True,
                ssl_expiry_thresholds=[30, 14, 7],
                domain_expiry_enabled=False,
                uptime_threshold_good=99.9,
                uptime_threshold_degraded=99.0,
                uptime_threshold_critical=95.0,
            ),
        )
        assert monitor.id
        assert monitor.check_interval_ms == 60000
        assert monitor.timeout_ms == 10000
        assert monitor.http_method == "GET"
        assert monitor.follow_redirects is True
        assert monitor.failure_threshold == 5
        assert monitor.latency_threshold_ms == 5000

        self.client.monitors.delete(self.team_id, monitor.id)


# ---------------------------------------------------------------------------
# User (whoami)
# ---------------------------------------------------------------------------


class TestUser:
    def test_whoami(self, client: Oack) -> None:
        user = client.user.whoami()
        assert user.id
