#!/usr/bin/env python3
"""
Apply Settings Use Case
Business logic for applying settings to a Firefox profile
"""

import logging
from typing import Dict
from pathlib import Path

from hardfox.domain.entities import Setting
from hardfox.domain.enums import SettingLevel
from hardfox.domain.repositories import IFirefoxRepository
from hardfox.application.mappers import SettingToPrefMapper

logger = logging.getLogger(__name__)


class ApplySettingsUseCase:
    """
    Use case for applying settings to a Firefox profile.

    BASE settings are written to prefs.js (one-time apply, user can modify
    them later in about:config). ADVANCED settings are written to user.js
    (locked, re-applied on every Firefox startup).
    """

    def __init__(
        self,
        firefox_repo: IFirefoxRepository,
        mapper: SettingToPrefMapper = None
    ):
        self.firefox_repo = firefox_repo
        self.mapper = mapper or SettingToPrefMapper()

    def execute(
        self,
        profile_path: Path,
        settings: Dict[str, Setting],
        level: SettingLevel = None
    ) -> Dict[str, int]:
        """
        Apply settings to Firefox profile.

        BASE settings go to prefs.js (merged with existing, user-modifiable).
        ADVANCED settings go to user.js (replaced entirely, locked).

        Args:
            profile_path: Path to Firefox profile directory
            settings: Dictionary of setting_key -> Setting entity
            level: Which level to apply (BASE, ADVANCED, or None for BOTH)

        Returns:
            Dictionary with counts: {"base_applied": N, "advanced_applied": M}
        """
        if not self.firefox_repo.validate_profile_path(profile_path):
            raise ValueError(f"Invalid Firefox profile path: {profile_path}")

        # TREAT ALL SETTINGS AS BASE (prefs.js)
        # We want to allow user modification, so everything goes to prefs.js
        # and we explicitly clear user.js to remove old locks.
        # FIX [HIGH-003]: Implement Sync Protection Logic
        # 1. Identify if Sync Protection is enabled (via internal flag)
        # 2. Filter out internal flags (hardfox.*) from being written to prefs.js
        # 3. If enabled, generate services.sync.prefs.sync.<key> = false for all settings
        
        sync_protection_key = "hardfox.sync_protection.enabled"
        sync_protection_enabled = False
        
        # Check for sync protection flag
        if sync_protection_key in settings:
            # Handle both boolean and string values just in case
            val = settings[sync_protection_key].value
            sync_protection_enabled = (val is True or str(val).lower() == 'true')
            
        # Separate settings into categories:
        # 1. Internal hardfox.* flags (not written to Firefox)
        # 2. Sync engine/control settings (services.sync.*) - written as-is
        # 3. Regular Firefox settings - written + auto-sync-protection generated
        regular_settings = []
        sync_settings = []

        for s in settings.values():
            if s.key.startswith("hardfox."):
                continue  # Internal flag, skip
            elif s.key.startswith("services.sync."):
                sync_settings.append(s)  # User's explicit sync choices
            else:
                regular_settings.append(s)

        base_prefs = {}

        # Write sync engine/control settings directly (user's explicit choices)
        if sync_settings:
            base_prefs.update(self.mapper.map_many(sync_settings))

        if regular_settings:
            base_prefs.update(self.mapper.map_many(regular_settings))

            # Apply Sync Protection if enabled:
            # Generate services.sync.prefs.sync.<key> = false for every
            # regular setting, UNLESS the user already has an explicit
            # sync control setting for that key.
            if sync_protection_enabled:
                logger.info("Master Sync Protection ENABLED: Generating sync-prevention prefs")
                explicit_sync_keys = {s.key for s in sync_settings}
                for setting in regular_settings:
                    sync_pref_key = f"services.sync.prefs.sync.{setting.key}"
                    # Don't overwrite user's explicit sync choice
                    if sync_pref_key not in explicit_sync_keys:
                        base_prefs[sync_pref_key] = False

        if base_prefs:
            self.firefox_repo.write_prefs(
                profile_path=profile_path,
                prefs=base_prefs,
                level=SettingLevel.BASE,
                merge=True
            )
            logger.info(
                f"Applied {len(base_prefs)} prefs "
                f"to prefs.js (BASE) in {profile_path.name}"
            )

        # Clear user.js (ADVANCED) to prevent locking
        # We write an empty dict with merge=False to overwrite the file
        self.firefox_repo.write_prefs(
            profile_path=profile_path,
            prefs={},
            level=SettingLevel.ADVANCED,
            merge=False
        )
        logger.info(f"Cleared user.js (ADVANCED) in {profile_path.name} to unlock settings")

        total_applied = len(base_prefs) if base_prefs else 0
        results = {
            "base_applied": total_applied,
            "advanced_applied": 0
        }

        if total_applied == 0:
            logger.info("No settings to apply")

        return results
