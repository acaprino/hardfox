#!/usr/bin/env python3
"""
Setting Level Enumeration
Defines whether settings are applied to prefs.js (BASE) or user.js (ADVANCED)
"""

from enum import Enum, auto


class SettingLevel(Enum):
    """
    Controls where settings are applied in Firefox profile.

    BASE: Applied to prefs.js (user-configurable in Firefox UI)
    ADVANCED: Applied to user.js (locked, loaded on every startup)
    """
    BASE = "BASE"
    ADVANCED = "ADVANCED"

    def __str__(self) -> str:
        return self.value

    @property
    def filename(self) -> str:
        """Returns the Firefox filename for this level.

        BASE settings are written to prefs.js (one-time apply, user can
        change them in about:config and Firefox preserves the changes).
        ADVANCED settings are written to user.js (re-applied on every
        Firefox startup, locking the value).
        """
        if self == SettingLevel.BASE:
            return "prefs.js"
        return "user.js"

    @property
    def prefix(self) -> str:
        """Returns the JavaScript function prefix for this level.

        prefs.js uses pref() - standard preference declaration.
        user.js uses user_pref() - user override that takes precedence.
        """
        if self == SettingLevel.BASE:
            return "pref"
        return "user_pref"
