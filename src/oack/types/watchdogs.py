"""Deprecated: Use oack.types.triggers instead."""

from oack.types.triggers import (
    CreateTriggerParams as CreateWatchdogParams,
)
from oack.types.triggers import (
    Trigger as Watchdog,
)
from oack.types.triggers import (
    UpdateTriggerParams as UpdateWatchdogParams,
)

__all__ = ["CreateWatchdogParams", "UpdateWatchdogParams", "Watchdog"]
