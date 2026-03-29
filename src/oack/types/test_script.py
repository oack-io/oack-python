"""Test script types."""

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel

if TYPE_CHECKING:
    from oack.types.browser_probes import ConsoleMessage, StepResult


class WebVitals(BaseModel):
    lcp_ms: float = 0
    fcp_ms: float = 0
    cls: float = 0
    ttfb_ms: float = 0


class TestScriptParams(BaseModel):
    script: str | None = None
    suite: str | None = None
    pw_project: str | None = None
    pw_grep: str | None = None
    env_overrides: dict[str, str] | None = None


class TestScriptResult(BaseModel):
    passed: bool
    total_ms: int = 0
    error: str = ""
    status: int = 0
    steps: list[StepResult] = []
    console_messages: list[ConsoleMessage] = []
    screenshot_url: str = ""
    report_url: str = ""
    test_count: int = 0
    pass_count: int = 0
    fail_count: int = 0
    skip_count: int = 0
    web_vitals: WebVitals | None = None


# Rebuild model to resolve forward references from TYPE_CHECKING imports.
def _rebuild() -> None:
    from oack.types.browser_probes import ConsoleMessage, StepResult

    TestScriptResult.model_rebuild(_types_namespace={"ConsoleMessage": ConsoleMessage, "StepResult": StepResult})


_rebuild()
del _rebuild
