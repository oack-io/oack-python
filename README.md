[![PyPI version](https://img.shields.io/pypi/v/oack.svg)](https://pypi.org/project/oack/)
[![Python versions](https://img.shields.io/pypi/pyversions/oack.svg)](https://pypi.org/project/oack/)
[![CI](https://github.com/oack-io/oack-python/actions/workflows/ci.yml/badge.svg)](https://github.com/oack-io/oack-python/actions/workflows/ci.yml)
[![License: MPL 2.0](https://img.shields.io/badge/License-MPL_2.0-brightgreen.svg)](https://opensource.org/licenses/MPL-2.0)
[![Checked with mypy](https://img.shields.io/badge/type--checked-mypy-blue.svg)](https://mypy-lang.org/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

# oack

Official Python client for the [Oack](https://oack.io) monitoring API.

## Installation

```bash
pip install oack
```

Or install from GitHub (always tracks the latest release):
```bash
pip install git+https://github.com/oack-io/oack-python.git@latest
```

## Quick Start

### Async (recommended)

```python
from oack import AsyncOack

async with AsyncOack(api_key="sk-...") as client:
    teams = await client.teams.list()
    for team in teams:
        print(team.id, team.name)
```

### Sync

```python
from oack import Oack

with Oack(api_key="sk-...") as client:
    teams = client.teams.list()
    for team in teams:
        print(team.id, team.name)
```

## Configuration

```python
client = AsyncOack(
    api_key="sk-...",
    base_url="https://api.oack.io",  # default
    timeout=30.0,                     # seconds, default
    max_retries=2,                    # default
)

# Dynamic token (e.g. refreshable JWT)
client = AsyncOack(api_key_func=lambda: get_current_jwt())
```

## Browser Login (Device Flow)

Authenticate via browser instead of a static API key. The JWT lives only in memory and disappears when the program exits.

```python
from oack import Oack, device_flow_authenticate

# Opens your browser, waits for approval, returns JWT
token = device_flow_authenticate()

with Oack(api_key=token) as client:
    teams = client.teams.list()
```

Async version:

```python
from oack import AsyncOack, async_device_flow_authenticate

token = await async_device_flow_authenticate()

async with AsyncOack(api_key=token) as client:
    teams = await client.teams.list()
```

## Error Handling

```python
from oack import AsyncOack, NotFoundError, RateLimitError, APIError

try:
    monitor = await client.monitors.get(team_id, monitor_id)
except NotFoundError:
    print("Monitor not found")
except RateLimitError as e:
    print(f"Rate limited, retry after {e.retry_after}s")
except APIError as e:
    print(f"API error {e.status_code}: {e.message}")
```

## Resources

| Resource | Access | Key Methods |
|----------|--------|-------------|
| Accounts | `client.accounts` | `create`, `list`, `get`, `update`, `delete`, `restore`, `transfer` |
| Teams | `client.teams` | `create`, `list`, `get`, `update`, `delete`, `list_members`, `add_member` |
| Monitors | `client.monitors` | `create`, `list`, `get`, `update`, `delete`, `pause`, `unpause`, `duplicate`, `move` |
| Probes | `client.probes` | `list`, `get`, `get_details`, `download_pcap`, `aggregate` |
| Alert Channels | `client.alert_channels` | `create`, `list`, `get`, `update`, `delete`, `test` |
| Metrics | `client.metrics` | `get_monitor_metrics`, `get_expiration`, `list_timeline`, chart events |
| Geo | `client.geo` | `list_checkers`, `list_regions` |

## Types

All response types are Pydantic v2 models with full IDE autocomplete:

```python
from oack.types import Monitor, Team, Probe, CreateMonitorParams
```
