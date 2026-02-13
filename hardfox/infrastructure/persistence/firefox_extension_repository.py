"""
Firefox extension repository implementation using profile sideloading.

Extensions are downloaded as .xpi files from AMO and placed in
{profile_path}/extensions/{extension_id}.xpi. Firefox picks them up on
next startup and the user retains full control via about:addons.

policies.json is only used for 3rdparty configuration (e.g. uBlock Origin
filter lists via toAdd).
"""
import json
import logging
import shutil
import tempfile
import urllib.request
import urllib.error
import zipfile
from pathlib import Path
from typing import Dict, List
from datetime import datetime
from urllib.parse import urlparse

from hardfox.domain.repositories.i_extension_repository import IExtensionRepository
from hardfox.domain.enums.extension_status import InstallationStatus
from hardfox.metadata.extensions_metadata import EXTENSIONS_METADATA
from hardfox.infrastructure.persistence.firefox_detection import get_firefox_installation_dir

logger = logging.getLogger(__name__)

# Timeout for downloading .xpi files from AMO (seconds)
_DOWNLOAD_TIMEOUT = 60

# Maximum number of policies.json backups to keep
_MAX_POLICY_BACKUPS = 5

# User-Agent sent when downloading from AMO
_USER_AGENT = "Hardfox/4.0 (Firefox Privacy Configurator)"


class FirefoxExtensionRepository(IExtensionRepository):
    """Manages Firefox extensions via profile sideloading + policies.json for 3rdparty config."""

    def install_extensions(
        self,
        profile_path: Path,
        extension_ids: List[str]
    ) -> Dict[str, InstallationStatus]:
        """
        Install extensions by downloading .xpi files into the profile's extensions/ directory.

        Also writes 3rdparty configuration to policies.json (e.g. uBlock Origin filter lists).

        Args:
            profile_path: Path to Firefox profile directory
            extension_ids: List of extension IDs to install

        Returns:
            Dictionary mapping extension IDs to installation status
        """
        results = {}

        try:
            if not profile_path.exists():
                logger.error(f"Profile path does not exist: {profile_path}")
                return {ext_id: InstallationStatus.FAILED for ext_id in extension_ids}

            extensions_dir = profile_path / "extensions"
            extensions_dir.mkdir(parents=True, exist_ok=True)

            for ext_id in extension_ids:
                if ext_id not in EXTENSIONS_METADATA:
                    logger.warning(f"Unknown extension ID: {ext_id}")
                    results[ext_id] = InstallationStatus.FAILED
                    continue

                ext_data = EXTENSIONS_METADATA[ext_id]
                install_url = ext_data["install_url"]

                if not self._is_valid_amo_url(install_url):
                    logger.error(f"Rejected non-AMO install URL for {ext_id}: {install_url}")
                    results[ext_id] = InstallationStatus.FAILED
                    continue

                # Download .xpi to profile extensions directory
                xpi_path = extensions_dir / f"{ext_id}.xpi"
                try:
                    self._download_xpi(install_url, xpi_path)
                    results[ext_id] = InstallationStatus.INSTALLED
                    logger.info(f"Sideloaded extension: {ext_id} -> {xpi_path}")
                except Exception as e:
                    logger.error(f"Failed to download {ext_id}: {e}")
                    results[ext_id] = InstallationStatus.FAILED

            # Write 3rdparty config (e.g. uBlock Origin filter lists)
            installed_ids = [
                ext_id for ext_id, status in results.items()
                if status == InstallationStatus.INSTALLED
            ]
            if installed_ids:
                try:
                    self._write_third_party_policies(profile_path, installed_ids)
                except Exception as e:
                    logger.warning(
                        f"Extensions installed but 3rdparty config failed: {e}. "
                        f"uBlock Origin filter lists may need manual configuration."
                    )

            return results

        except Exception as e:
            logger.error(f"Failed to install extensions: {e}")
            return {ext_id: InstallationStatus.FAILED for ext_id in extension_ids}

    def uninstall_extensions(
        self,
        profile_path: Path,
        extension_ids: List[str]
    ) -> Dict[str, InstallationStatus]:
        """
        Uninstall extensions by removing .xpi files from the profile's extensions/ directory.

        Also removes any 3rdparty configuration from policies.json.

        Args:
            profile_path: Path to Firefox profile directory
            extension_ids: List of extension IDs to uninstall

        Returns:
            Dictionary mapping extension IDs to uninstallation status
        """
        try:
            if not profile_path.exists():
                logger.error(f"Profile path does not exist: {profile_path}")
                return {ext_id: InstallationStatus.FAILED for ext_id in extension_ids}

            extensions_dir = profile_path / "extensions"
            results = {}

            for ext_id in extension_ids:
                xpi_path = extensions_dir / f"{ext_id}.xpi"
                try:
                    if xpi_path.exists():
                        xpi_path.unlink()
                        logger.info(f"Removed sideloaded extension: {ext_id}")
                    else:
                        logger.info(f"Extension .xpi not found (already removed?): {ext_id}")
                    results[ext_id] = InstallationStatus.UNINSTALLED
                except Exception as e:
                    logger.error(f"Failed to remove {ext_id}: {e}")
                    results[ext_id] = InstallationStatus.FAILED

            # Remove 3rdparty config for uninstalled extensions
            self._remove_third_party_policies(profile_path, extension_ids)

            return results

        except Exception as e:
            logger.error(f"Failed to uninstall extensions: {e}")
            return {ext_id: InstallationStatus.FAILED for ext_id in extension_ids}

    def get_installed_extensions(
        self,
        profile_path: Path
    ) -> List[str]:
        """
        Get list of known extension IDs sideloaded in the profile's extensions/ directory.

        Only returns IDs that are also present in EXTENSIONS_METADATA.

        Args:
            profile_path: Path to Firefox profile directory

        Returns:
            List of extension IDs with .xpi files in the profile
        """
        try:
            if not profile_path.exists():
                logger.error(f"Profile path does not exist: {profile_path}")
                return []

            extensions_dir = profile_path / "extensions"
            if not extensions_dir.exists():
                return []

            installed = []
            for ext_id in EXTENSIONS_METADATA:
                xpi_path = extensions_dir / f"{ext_id}.xpi"
                if xpi_path.exists():
                    installed.append(ext_id)

            logger.info(f"Found {len(installed)} sideloaded extensions in profile")
            return installed

        except Exception as e:
            logger.error(f"Failed to read installed extensions: {e}")
            return []

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _is_valid_amo_url(url: str) -> bool:
        """
        Validate that a URL is strictly from addons.mozilla.org.

        Prevents bypasses like addons.mozilla.org.evil.com or
        addons.mozilla.org@evil.com.
        """
        try:
            parsed = urlparse(url)
            return (
                parsed.scheme == "https"
                and parsed.netloc == "addons.mozilla.org"
                and parsed.path.startswith("/firefox/downloads/")
            )
        except Exception:
            return False

    def _download_xpi(self, url: str, dest: Path) -> None:
        """
        Download an .xpi file from AMO to a temp file, validate it as a
        valid ZIP archive, then atomically move it to the destination.

        Args:
            url: AMO download URL
            dest: Destination file path

        Raises:
            ValueError: If the downloaded file is not a valid XPI/ZIP archive
            urllib.error.URLError: If the download fails
        """
        logger.info(f"Downloading {url}")
        req = urllib.request.Request(url, headers={"User-Agent": _USER_AGENT})

        # Download to temp file in the same directory (ensures same filesystem for rename)
        tmp_fd, tmp_path_str = tempfile.mkstemp(suffix=".xpi.tmp", dir=dest.parent)
        tmp_path = Path(tmp_path_str)
        try:
            with urllib.request.urlopen(req, timeout=_DOWNLOAD_TIMEOUT) as response:
                with open(tmp_fd, "wb") as f:
                    shutil.copyfileobj(response, f)

            # Validate the downloaded file is a valid ZIP (XPI is ZIP format)
            if not zipfile.is_zipfile(tmp_path):
                raise ValueError(
                    f"Downloaded file is not a valid XPI/ZIP archive: {url}"
                )

            # Atomic move to final destination
            shutil.move(tmp_path, dest)
            logger.info(f"Verified and saved: {dest}")
        finally:
            # Clean up temp file if still present (download failed or validation failed)
            if tmp_path.exists():
                try:
                    tmp_path.unlink()
                except OSError:
                    pass

    def _write_third_party_policies(
        self,
        profile_path: Path,
        installed_ext_ids: List[str]
    ) -> None:
        """
        Write 3rdparty extension config (e.g. uBO filter lists) to policies.json.

        Only writes if there is actual 3rdparty config to set.

        Raises:
            Exception: If Firefox installation dir is not found or write fails.
        """
        third_party_config = self._build_third_party_config(installed_ext_ids)
        if not third_party_config:
            return

        firefox_dir = get_firefox_installation_dir(profile_path)
        if not firefox_dir:
            raise FileNotFoundError(
                "Could not locate Firefox installation directory for 3rdparty policies"
            )

        dist_dir = firefox_dir / "distribution"
        dist_dir.mkdir(parents=True, exist_ok=True)
        policies_file = dist_dir / "policies.json"

        existing_policies = self._read_existing_policies(policies_file)

        if policies_file.exists():
            self._backup_policies(policies_file)

        # Ensure structure
        if "policies" not in existing_policies:
            existing_policies["policies"] = {}

        # Remove any leftover ExtensionSettings from old Hardfox versions
        existing_policies["policies"].pop("ExtensionSettings", None)

        # Set 3rdparty config
        if "3rdparty" not in existing_policies["policies"]:
            existing_policies["policies"]["3rdparty"] = {"Extensions": {}}
        if "Extensions" not in existing_policies["policies"]["3rdparty"]:
            existing_policies["policies"]["3rdparty"]["Extensions"] = {}

        existing_policies["policies"]["3rdparty"]["Extensions"].update(third_party_config)
        logger.info(f"Writing 3rdparty config for {len(third_party_config)} extensions")

        with open(policies_file, "w", encoding="utf-8") as f:
            json.dump(existing_policies, f, indent=2)

    def _remove_third_party_policies(
        self,
        profile_path: Path,
        extension_ids: List[str]
    ) -> None:
        """Remove 3rdparty config entries for the given extensions from policies.json."""
        firefox_dir = get_firefox_installation_dir(profile_path)
        if not firefox_dir:
            return

        policies_file = firefox_dir / "distribution" / "policies.json"
        if not policies_file.exists():
            return

        existing_policies = self._read_existing_policies(policies_file)
        third_party_exts = (
            existing_policies.get("policies", {})
            .get("3rdparty", {})
            .get("Extensions", {})
        )

        changed = False
        for ext_id in extension_ids:
            if ext_id in third_party_exts:
                del third_party_exts[ext_id]
                changed = True

        if not changed:
            return

        # Clean up empty structures
        if not third_party_exts:
            existing_policies["policies"]["3rdparty"].pop("Extensions", None)
            if not existing_policies["policies"]["3rdparty"]:
                existing_policies["policies"].pop("3rdparty", None)

        # Also clean up leftover ExtensionSettings from old versions
        existing_policies["policies"].pop("ExtensionSettings", None)

        # Remove policies.json entirely if empty
        if not existing_policies.get("policies"):
            try:
                policies_file.unlink()
                logger.info("Removed empty policies.json")
            except Exception as e:
                logger.warning(f"Failed to remove empty policies.json: {e}")
            return

        self._backup_policies(policies_file)
        with open(policies_file, "w", encoding="utf-8") as f:
            json.dump(existing_policies, f, indent=2)
        logger.info(f"Removed 3rdparty config for {len(extension_ids)} extensions")

    def _build_third_party_config(self, extension_ids: List[str]) -> dict:
        """
        Build 3rdparty extension configuration for extensions that support it.

        Currently supports uBlock Origin filter lists via toAdd (non-locking).
        """
        config = {}

        for ext_id in extension_ids:
            if ext_id not in EXTENSIONS_METADATA:
                continue

            ext_data = EXTENSIONS_METADATA[ext_id]

            if ext_id == "uBlock0@raymondhill.net":
                builtin_lists = ext_data.get("builtin_filter_lists", [])
                custom_lists = ext_data.get("custom_filter_lists", [])

                if builtin_lists or custom_lists:
                    selected_lists = ["user-filters"] + list(builtin_lists) + list(custom_lists)

                    # toAdd only: sets initial defaults without overwriting user changes
                    config[ext_id] = {
                        "toAdd": {
                            "filterLists": selected_lists
                        }
                    }
                    logger.info(
                        f"Configured uBlock Origin with {len(selected_lists)} filter lists "
                        f"(toAdd — user can modify freely)"
                    )

        return config

    def _read_existing_policies(self, policies_file: Path) -> dict:
        """Read existing policies.json file."""
        if not policies_file.exists():
            return {"policies": {}}

        try:
            with open(policies_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, Exception) as e:
            logger.warning(f"Failed to parse policies.json, starting fresh: {e}")
            return {"policies": {}}

    def _backup_policies(self, policies_file: Path) -> None:
        """Create timestamped backup of policies.json (keeps last _MAX_POLICY_BACKUPS)."""
        if not policies_file.exists():
            return

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = policies_file.with_name(f"policies.json.backup.{timestamp}")

        try:
            shutil.copy2(policies_file, backup_file)
            logger.info(f"Created backup: {backup_file}")

            # Rotate old backups
            backup_files = sorted(
                policies_file.parent.glob("policies.json.backup.*"),
                key=lambda p: p.stat().st_mtime,
                reverse=True
            )
            for old_backup in backup_files[_MAX_POLICY_BACKUPS:]:
                old_backup.unlink()
                logger.info(f"Removed old backup: {old_backup}")
        except Exception as e:
            logger.error(f"Failed to create backup: {e}")
