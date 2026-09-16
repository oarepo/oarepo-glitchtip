# SPDX-FileCopyrightText: 2026 CESNET z.s.p.o.
# SPDX-License-Identifier: MIT

from __future__ import annotations

from types import SimpleNamespace

from oarepo_glitchtip import ext


def test_add_anonymous_user_to_glitchtip(monkeypatch):
    sentry_users = []
    monkeypatch.setattr(ext, "current_user", SimpleNamespace(is_authenticated=False))
    monkeypatch.setattr(ext.sentry_sdk, "set_user", sentry_users.append)

    ext.add_user_to_glitchtip()

    assert sentry_users == [{"ip_address": "{{auto}}"}]


def test_add_authenticated_user_to_glitchtip(monkeypatch):
    user = SimpleNamespace(
        is_authenticated=True,
        id=1,
        email="user@example.org",
        user_profile={"full_name": "Test User"},
    )
    sentry_users = []
    monkeypatch.setattr(ext, "current_user", user)
    monkeypatch.setattr(ext.sentry_sdk, "set_user", sentry_users.append)

    ext.add_user_to_glitchtip()

    assert sentry_users == [
        {
            "id": 1,
            "email": "user@example.org",
            "username": "user@example.org",
            "ip_address": "{{auto}}",
            "full_name": "Test User",
        }
    ]
