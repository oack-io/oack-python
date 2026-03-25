"""Oack API error types."""

from __future__ import annotations


class OackError(Exception):
    """Base exception for all Oack errors."""


class APIError(OackError):
    """Non-2xx response from the Oack API."""

    def __init__(self, status_code: int, message: str) -> None:
        self.status_code = status_code
        self.message = message
        super().__init__(f"oack API error ({status_code}): {message}" if message else f"oack API error ({status_code})")


class AuthenticationError(APIError):
    """401 Unauthorized."""

    def __init__(self, message: str = "unauthorized") -> None:
        super().__init__(401, message)


class ForbiddenError(APIError):
    """403 Forbidden."""

    def __init__(self, message: str = "forbidden") -> None:
        super().__init__(403, message)


class NotFoundError(APIError):
    """404 Not Found."""

    def __init__(self, message: str = "not found") -> None:
        super().__init__(404, message)


class ConflictError(APIError):
    """409 Conflict."""

    def __init__(self, message: str = "conflict") -> None:
        super().__init__(409, message)


class RateLimitError(APIError):
    """429 Too Many Requests."""

    retry_after: float | None

    def __init__(self, message: str = "rate limited", retry_after: float | None = None) -> None:
        self.retry_after = retry_after
        super().__init__(429, message)


_STATUS_MAP: dict[int, type[APIError]] = {
    401: AuthenticationError,
    403: ForbiddenError,
    404: NotFoundError,
    409: ConflictError,
    429: RateLimitError,
}


def _parse_error(status_code: int, body: bytes, retry_after: float | None = None) -> APIError:
    """Parse an API error response."""
    import json

    message = ""
    try:
        data = json.loads(body)
        message = data.get("error", "") or data.get("message", "")
    except (json.JSONDecodeError, AttributeError):
        message = body.decode("utf-8", errors="replace")

    cls = _STATUS_MAP.get(status_code, APIError)
    if cls is RateLimitError:
        return RateLimitError(message or "rate limited", retry_after=retry_after)
    if cls is not APIError:
        return cls(message)
    return APIError(status_code, message)
