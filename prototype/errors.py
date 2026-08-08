"""Structured VIAL error model (SDK-001 §30, §31).

VIALError carries a machine-readable `code`, a human `message`, an optional
`request_id` for correlation, and optional `details`. Error categories follow
SDK-001 §30:

    Authentication, Authorization, Validation, Runtime, Network,
    Timeout, Conflict, Unavailable

Concrete exception types subclass VIALError for catchable semantics while
retaining Python built-in compatibility where useful.
"""
from __future__ import annotations

from typing import Any

# SDK-001 §30 error categories
AUTHENTICATION = "authentication"
AUTHORIZATION = "authorization"
VALIDATION = "validation"
RUNTIME = "runtime"
NETWORK = "network"
TIMEOUT = "timeout"
CONFLICT = "conflict"
UNAVAILABLE = "unavailable"


class VIALError(Exception):
    """Base structured error for the VIAL SDK (SDK-001 §30)."""

    category: str = RUNTIME

    def __init__(self, code: str, message: str, request_id: str | None = None,
                 details: dict[str, Any] | None = None):
        super().__init__(message)
        self.code = code
        self.message = message
        self.request_id = request_id
        self.details = details or {}

    def to_dict(self) -> dict:
        payload = {
            "code": self.code,
            "message": self.message,
            "category": self.category,
        }
        if self.request_id is not None:
            payload["request_id"] = self.request_id
        if self.details:
            payload["details"] = self.details
        return payload


class VIALAuthenticationError(VIALError, PermissionError):
    """Raised when a caller cannot be authenticated (SDK-001 §30)."""

    category = AUTHENTICATION


class VIALAuthorizationError(VIALError, PermissionError):
    """Raised when an actor lacks authority (SDK-001 §30 - Authorization)."""

    category = AUTHORIZATION


class VIALValidationError(VIALError, ValueError):
    """Raised for invalid input or impossible operations (Validation)."""

    category = VALIDATION


class VIALConflictError(VIALError, ValueError):
    """Raised for concurrent/state conflicts (SDK-001 §30 - Conflict)."""

    category = CONFLICT


class VIALStateError(VIALError, KeyError):
    """Raised when a State element is missing or unknown (SDK-001 §30)."""

    category = RUNTIME


class VIALExecutionError(VIALError, RuntimeError):
    """Raised when an execution resource cannot complete an operation."""

    category = RUNTIME


class VIALNetworkError(VIALError, ConnectionError):
    """Raised when a transport call fails (SDK-001 §30 - Network)."""

    category = NETWORK


class VIALTimeoutError(VIALError, TimeoutError):
    """Raised when an operation exceeds its deadline (SDK-001 §30 - Timeout)."""

    category = TIMEOUT


class VIALUnavailableError(VIALError, RuntimeError):
    """Raised when a resource is not available (SDK-001 §30 - Unavailable)."""

    category = UNAVAILABLE


def wrap_network_error(exc: Exception, message: str | None = None,
                       request_id: str | None = None,
                       details: dict[str, Any] | None = None) -> VIALError:
    """Wrap a raw transport exception into the structured VIAL error model
    (SDK-001 §31). Returns the original exception if it is already a VIALError."""
    if isinstance(exc, VIALError):
        return exc
    if isinstance(exc, TimeoutError):
        return VIALTimeoutError(
            "TIMEOUT", message or str(exc), request_id=request_id, details=details)
    if isinstance(exc, ConnectionError):
        return VIALNetworkError(
            "NETWORK_ERROR", message or str(exc), request_id=request_id, details=details)
    return VIALExecutionError(
        "EXECUTION_ERROR", message or str(exc), request_id=request_id, details=details)
