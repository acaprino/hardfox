#!/usr/bin/env python3
"""
Customize ViewModel
State management for Screen 2 (Customize Settings)
"""

from typing import Dict, List, Optional
from .base_view_model import BaseViewModel
from hardzilla.domain.entities import Setting, Profile


class CustomizeViewModel(BaseViewModel):
    """
    ViewModel for the Customize screen (Screen 2).

    Manages the state of 140+ settings with modifications tracking.

    Properties:
    - profile: Current profile being customized (optional, for metadata only)
    - settings: Dictionary of all settings (key -> Setting)
    - modified_settings: Set of keys that have been modified
    - search_query: Current search filter text
    - selected_category: Currently expanded category
    - show_advanced: Whether to show advanced settings
    """

    def __init__(self, settings_repo=None):
        """
        Initialize customize view model.

        Args:
            settings_repo: Repository to load all available settings
        """
        super().__init__()

        # Load all settings from metadata
        all_settings = settings_repo.get_all() if settings_repo else {}

        self._properties = {
            'profile': None,
            'settings': all_settings.copy(),  # Start with all settings at default values
            'base_settings': all_settings,  # Keep reference to base metadata
            'modified_settings': set(),
            'search_query': '',
            'selected_category': None,
            'show_advanced': False,
            'modification_count': 0
        }

    # Profile
    @property
    def profile(self) -> Optional[Profile]:
        return self.get_property('profile')

    @profile.setter
    def profile(self, value: Optional[Profile]):
        """
        Set profile and UPDATE setting values (not replace).

        When a preset is selected or Firefox profile is imported,
        this updates the values of the settings without replacing
        the entire settings dictionary.
        """
        self.set_property('profile', value)
        if value:
            # Update values from the profile settings
            current_settings = self._properties['settings']
            for key, profile_setting in value.settings.items():
                if key in current_settings:
                    # Update existing setting value
                    current_settings[key] = profile_setting
                else:
                    # Add new setting if not in metadata
                    current_settings[key] = profile_setting

            self._notify('settings', self._properties['settings'])

    # Settings
    @property
    def settings(self) -> Dict[str, Setting]:
        return self.get_property('settings', {})

    def get_setting(self, key: str) -> Optional[Setting]:
        """Get a setting by key"""
        return self.settings.get(key)

    def update_setting_value(self, key: str, new_value) -> None:
        """
        Update a setting value and mark as modified.

        Args:
            key: Setting key to update
            new_value: New value for the setting
        """
        if key in self.settings:
            setting = self.settings[key]
            updated_setting = setting.clone_with_value(new_value)
            self._properties['settings'][key] = updated_setting

            # Track modification
            modified = self.get_property('modified_settings', set())
            modified.add(key)
            self.set_property('modified_settings', modified)
            self.set_property('modification_count', len(modified))

            self._notify('settings', self._properties['settings'])

    def reset_setting(self, key: str) -> None:
        """Reset a setting to its original value"""
        if self.profile and key in self.profile.settings:
            original = self.profile.settings[key]
            self._properties['settings'][key] = original

            # Remove from modified set
            modified = self.get_property('modified_settings', set())
            modified.discard(key)
            self.set_property('modified_settings', modified)
            self.set_property('modification_count', len(modified))

            self._notify('settings', self._properties['settings'])

    def reset_all(self) -> None:
        """Reset all settings to current profile values (or defaults if no profile)"""
        if self.profile:
            # Reset to profile values
            current_settings = self._properties['settings']
            for key, profile_setting in self.profile.settings.items():
                if key in current_settings:
                    current_settings[key] = profile_setting
        else:
            # Reset to base metadata defaults
            self._properties['settings'] = self._properties['base_settings'].copy()

        self.set_property('modified_settings', set())
        self.set_property('modification_count', 0)
        self._notify('settings', self._properties['settings'])

    # Search Query
    @property
    def search_query(self) -> str:
        return self.get_property('search_query', '')

    @search_query.setter
    def search_query(self, value: str):
        self.set_property('search_query', value)

    def get_filtered_settings(self) -> Dict[str, Setting]:
        """Get settings filtered by search query"""
        query = self.search_query.lower()
        if not query:
            return self.settings

        return {
            key: setting
            for key, setting in self.settings.items()
            if (query in key.lower() or
                query in setting.description.lower() or
                query in setting.category.lower())
        }

    # Selected Category
    @property
    def selected_category(self) -> Optional[str]:
        return self.get_property('selected_category')

    @selected_category.setter
    def selected_category(self, value: Optional[str]):
        self.set_property('selected_category', value)

    def get_settings_by_category(self, category: str) -> List[Setting]:
        """Get all settings for a specific category"""
        return [
            setting
            for setting in self.settings.values()
            if setting.category == category
        ]

    # Show Advanced
    @property
    def show_advanced(self) -> bool:
        return self.get_property('show_advanced', False)

    @show_advanced.setter
    def show_advanced(self, value: bool):
        self.set_property('show_advanced', value)

    # Modification Count
    @property
    def modification_count(self) -> int:
        return self.get_property('modification_count', 0)

    @property
    def has_modifications(self) -> bool:
        """Check if any settings have been modified"""
        return self.modification_count > 0
