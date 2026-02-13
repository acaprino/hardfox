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

        # Collect settings by level
        base_settings = []
        advanced_settings = []

        for s in settings.values():
            if s.level == SettingLevel.BASE and (level is None or level == SettingLevel.BASE):
                base_settings.append(s)
            elif s.level == SettingLevel.ADVANCED and (level is None or level == SettingLevel.ADVANCED):
                advanced_settings.append(s)

        # Apply BASE settings to prefs.js (merge with existing)
        if base_settings:
            base_prefs = self.mapper.map_many(base_settings)
            self.firefox_repo.write_prefs(
                profile_path=profile_path,
                prefs=base_prefs,
                level=SettingLevel.BASE,
                merge=True
            )
            logger.info(
                f"Applied {len(base_settings)} BASE settings to prefs.js "
                f"in {profile_path.name}"
            )

        # Apply ADVANCED settings to user.js (replace entirely)
        if advanced_settings:
            advanced_prefs = self.mapper.map_many(advanced_settings)
            self.firefox_repo.write_prefs(
                profile_path=profile_path,
                prefs=advanced_prefs,
                level=SettingLevel.ADVANCED,
                merge=False
            )
            logger.info(
                f"Applied {len(advanced_settings)} ADVANCED settings to user.js "
                f"in {profile_path.name}"
            )

        results = {
            "base_applied": len(base_settings),
            "advanced_applied": len(advanced_settings)
        }

        if not base_settings and not advanced_settings:
            logger.info("No settings to apply")

        return results
