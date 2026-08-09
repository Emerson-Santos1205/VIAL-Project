"""Minimal authenticated identity boundary (SDK-001 §30)."""
from __future__ import annotations

import hashlib
import hmac
import os
from dataclasses import dataclass

from .errors import VIALAuthorizationError, VIALValidationError


@dataclass(frozen=True)
class Principal:
    """Authenticated actor presented to the authorization boundary."""
    actor: str
    organization_id: str


class Authenticator:
    """Small stdlib authenticator for local reference deployments.

    Production deployments should replace the credential source with an
    external identity provider; the authorization contract remains the same.
    """

    def __init__(self, iterations: int = 120_000):
        self.iterations = iterations
        self._credentials: dict[str, tuple[str, str, str]] = {}

    def register(self, actor: str, organization_id: str, secret: str) -> None:
        if not actor or not organization_id or not secret:
            raise VIALValidationError(
                "INVALID_IDENTITY", "actor, organization and secret are required")
        salt = os.urandom(16).hex()
        digest = self._derive(secret, salt)
        self._credentials[actor] = (organization_id, salt, digest)

    def authenticate(self, actor: str, secret: str) -> Principal:
        credential = self._credentials.get(actor)
        if credential is None:
            raise VIALAuthorizationError(
                "AUTHENTICATION_FAILED", "unknown actor")
        organization_id, salt, expected = credential
        actual = self._derive(secret, salt)
        if not hmac.compare_digest(actual, expected):
            raise VIALAuthorizationError(
                "AUTHENTICATION_FAILED", "invalid credentials")
        return Principal(actor=actor, organization_id=organization_id)

    def _derive(self, secret: str, salt: str) -> str:
        return hashlib.pbkdf2_hmac(
            "sha256", secret.encode(), salt.encode(), self.iterations).hex()
