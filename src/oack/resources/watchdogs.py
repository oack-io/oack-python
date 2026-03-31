"""Deprecated: Use oack.resources.triggers instead."""

from oack.resources.triggers import (
    AsyncTriggers as AsyncWatchdogs,
)
from oack.resources.triggers import (
    Triggers as Watchdogs,
)

__all__ = ["AsyncWatchdogs", "Watchdogs"]
