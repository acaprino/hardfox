#!/usr/bin/env python3
"""
Pref to Setting Mapper
Converts Firefox preferences to Setting entities
"""

import logging
from typing import Dict, Any, Optional
from hardzilla.domain.entities import Setting
from hardzilla.domain.repositories import ISettingsRepository

logger = logging.getLogger(__name__)


class PrefToSettingMapper:
    """Maps Firefox preferences to Setting entities"""

    def __init__(self, settings_repo: ISettingsRepository):
        """
        Initialize mapper.

        Args:
            settings_repo: Repository providing setting metadata
        """
        self.settings_repo = settings_repo

    def map(self, pref_key: str, pref_value: Any) -> Optional[Setting]:
        """
        Convert Firefox preference to Setting entity.

        Args:
            pref_key: Firefox preference key
            pref_value: Firefox preference value

        Returns:
            Setting entity if pref is known, None otherwise
        """
        from hardzilla.domain.enums import SettingType

        # Get metadata for this preference
        metadata_setting = self.settings_repo.get_by_key(pref_key)

        if metadata_setting is None:
            logger.debug(f"Unknown preference '{pref_key}', skipping")
            return None

        # Normalize dropdown values (case-insensitive matching)
        if metadata_setting.setting_type == SettingType.DROPDOWN:
            pref_value = self._normalize_dropdown_value(pref_value, metadata_setting.options)

        # Create new setting with imported value
        return metadata_setting.clone_with_value(pref_value)

    def _normalize_dropdown_value(self, value: Any, options: list) -> Any:
        """
        Normalize dropdown value to match available options (case-insensitive).

        Args:
            value: The value to normalize
            options: List of valid options

        Returns:
            Normalized value that matches one of the options, or original value if no match
        """
        if not isinstance(value, str) or not options:
            return value

        # Try exact match first
        if value in options:
            return value

        # Try case-insensitive match
        value_lower = value.lower()
        for option in options:
            if isinstance(option, str) and option.lower() == value_lower:
                return option

        # No match found, return original (will fail validation)
        logger.warning(f"Could not normalize dropdown value '{value}' to options {options}")
        return value

    def map_many(self, prefs: Dict[str, Any]) -> Dict[str, Setting]:
        """
        Convert multiple Firefox preferences to Settings.

        Args:
            prefs: Dictionary of pref_key -> pref_value

        Returns:
            Dictionary of pref_key -> Setting entity (only known prefs)
        """
        settings = {}

        for pref_key, pref_value in prefs.items():
            setting = self.map(pref_key, pref_value)
            if setting is not None:
                settings[pref_key] = setting

        logger.info(
            f"Mapped {len(settings)} known preferences out of {len(prefs)} total"
        )

        return settings
