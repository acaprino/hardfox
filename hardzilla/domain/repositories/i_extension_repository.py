"""
Extension repository interface.
"""
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, List

from hardzilla.domain.enums.extension_status import InstallationStatus


class IExtensionRepository(ABC):
    """Interface for extension installation operations."""

    @abstractmethod
    def install_extensions(
        self,
        profile_path: Path,
        extension_ids: List[str]
    ) -> Dict[str, InstallationStatus]:
        """
        Install extensions to Firefox using policies.json.

        Args:
            profile_path: Path to Firefox profile directory
            extension_ids: List of extension IDs to install

        Returns:
            Dictionary mapping extension IDs to installation status
        """
        pass
