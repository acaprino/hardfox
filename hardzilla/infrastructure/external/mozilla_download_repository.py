#!/usr/bin/env python3
"""
Mozilla Download Repository

Downloads and extracts Firefox installers from Mozilla's CDN.
Uses only stdlib (urllib, hashlib) to avoid extra dependencies.

Security:
- Downloads over HTTPS from Mozilla's official CDN
- Verifies SHA-512 hash against Mozilla's published checksums
- Validates version strings with strict regex before use
"""

import hashlib
import json
import logging
import re
import shutil
import subprocess
import threading
import urllib.error
import urllib.request
from pathlib import Path
from typing import Callable, Dict, Optional

logger = logging.getLogger(__name__)

VERSIONS_URL = "https://product-details.mozilla.org/1.0/firefox_versions.json"
DOWNLOAD_URL_TEMPLATE = (
    "https://download-installer.cdn.mozilla.net/pub/firefox/releases/"
    "{version}/win64/en-US/Firefox%20Setup%20{version}.exe"
)
SHA512_URL_TEMPLATE = (
    "https://download-installer.cdn.mozilla.net/pub/firefox/releases/"
    "{version}/SHA512SUMS"
)
# Strict version format: digits.digits with optional .digits patch
VERSION_RE = re.compile(r'^\d+\.\d+(\.\d+)?$')


def validate_version(version: str) -> None:
    """
    Validate a Firefox version string.

    Raises:
        ValueError: If the version doesn't match expected format
    """
    if not version or not VERSION_RE.match(version):
        raise ValueError(f"Invalid Firefox version format: {version!r}")


class MozillaDownloadRepository:
    """
    Repository for downloading and extracting Firefox from Mozilla CDN.
    """

    def get_latest_version(self) -> Dict[str, str]:
        """
        Fetch the latest Firefox release version from Mozilla's API.

        Returns:
            Dict with 'version' and 'channel' keys.

        Raises:
            ConnectionError: If the API is unreachable or returns bad data
        """
        try:
            req = urllib.request.Request(
                VERSIONS_URL,
                headers={"User-Agent": "Hardzilla/1.0"}
            )
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = json.loads(resp.read().decode("utf-8"))

            version = data.get("LATEST_FIREFOX_VERSION", "")
            if not version:
                raise ValueError("LATEST_FIREFOX_VERSION not found in API response")

            validate_version(version)

            logger.info(f"Latest Firefox version from API: {version}")
            return {"version": version, "channel": "release"}

        except urllib.error.URLError as e:
            raise ConnectionError(f"Failed to reach Mozilla API: {e}") from e
        except (json.JSONDecodeError, ValueError) as e:
            raise ConnectionError(f"Invalid API response: {e}") from e

    def _fetch_expected_hash(self, version: str) -> Optional[str]:
        """
        Fetch the expected SHA-512 hash for the win64 en-US installer.

        Args:
            version: Firefox version string

        Returns:
            Hex-encoded SHA-512 hash, or None if not available
        """
        url = SHA512_URL_TEMPLATE.format(version=version)
        installer_filename = f"win64/en-US/Firefox Setup {version}.exe"

        try:
            req = urllib.request.Request(
                url,
                headers={"User-Agent": "Hardzilla/1.0"}
            )
            with urllib.request.urlopen(req, timeout=15) as resp:
                content = resp.read().decode("utf-8")

            for line in content.splitlines():
                # Format: "<sha512_hash>  <relative_path>"
                parts = line.split("  ", 1)
                if len(parts) == 2 and parts[1].strip() == installer_filename:
                    expected_hash = parts[0].strip().lower()
                    if len(expected_hash) == 128:  # SHA-512 is 128 hex chars
                        logger.info(f"Found SHA-512 hash for {installer_filename}")
                        return expected_hash

            logger.warning(f"SHA-512 hash not found for {installer_filename} in SHA512SUMS")
            return None

        except (urllib.error.URLError, OSError) as e:
            logger.warning(f"Could not fetch SHA512SUMS: {e}")
            return None

    def _verify_hash(self, file_path: Path, expected_hash: str) -> bool:
        """
        Verify SHA-512 hash of a downloaded file.

        Args:
            file_path: Path to file to verify
            expected_hash: Expected hex-encoded SHA-512 hash

        Returns:
            True if hash matches
        """
        sha512 = hashlib.sha512()
        with open(file_path, "rb") as f:
            while True:
                chunk = f.read(64 * 1024)
                if not chunk:
                    break
                sha512.update(chunk)

        actual_hash = sha512.hexdigest().lower()
        if actual_hash == expected_hash:
            logger.info(f"SHA-512 verification passed for {file_path.name}")
            return True

        logger.error(
            f"SHA-512 mismatch for {file_path.name}!\n"
            f"  Expected: {expected_hash}\n"
            f"  Actual:   {actual_hash}"
        )
        return False

    def download_installer(
        self,
        version: str,
        dest_path: Path,
        progress_cb: Optional[Callable[[str, float], None]] = None,
        cancel_event: Optional[threading.Event] = None
    ) -> Path:
        """
        Download the Firefox installer for the given version.

        Downloads the installer and verifies its SHA-512 hash against
        Mozilla's published checksums.

        Args:
            version: Firefox version string (e.g. "133.0")
            dest_path: Directory to save the installer in
            progress_cb: Progress callback(status, progress_0_to_1)
            cancel_event: Threading event to signal cancellation

        Returns:
            Path to the downloaded and verified installer exe

        Raises:
            ConnectionError: If download fails
            RuntimeError: If cancelled or hash verification fails
        """
        validate_version(version)

        url = DOWNLOAD_URL_TEMPLATE.format(version=version)
        dest_path.mkdir(parents=True, exist_ok=True)
        installer_path = dest_path / f"Firefox_Setup_{version}.exe"

        logger.info(f"Downloading Firefox {version} from: {url}")

        # Fetch expected hash before downloading
        expected_hash = self._fetch_expected_hash(version)

        if progress_cb:
            progress_cb(f"Downloading Firefox {version}...", 0.0)

        max_retries = 2
        for attempt in range(1, max_retries + 1):
            try:
                req = urllib.request.Request(
                    url,
                    headers={"User-Agent": "Hardzilla/1.0"}
                )
                with urllib.request.urlopen(req, timeout=60) as resp:
                    total_size = int(resp.headers.get("Content-Length", 0))
                    downloaded = 0
                    chunk_size = 64 * 1024  # 64 KB chunks

                    with open(installer_path, "wb") as f:
                        while True:
                            if cancel_event and cancel_event.is_set():
                                installer_path.unlink(missing_ok=True)
                                raise RuntimeError("Download cancelled by user")

                            chunk = resp.read(chunk_size)
                            if not chunk:
                                break

                            f.write(chunk)
                            downloaded += len(chunk)

                            if progress_cb and total_size > 0:
                                pct = downloaded / total_size
                                size_mb = downloaded / (1024 * 1024)
                                total_mb = total_size / (1024 * 1024)
                                progress_cb(
                                    f"Downloading: {size_mb:.1f} / {total_mb:.1f} MB",
                                    pct * 0.6  # Download is 60% of total update progress
                                )

                logger.info(f"Downloaded installer: {installer_path} ({downloaded} bytes)")
                break  # Success, exit retry loop

            except urllib.error.URLError as e:
                installer_path.unlink(missing_ok=True)
                if attempt < max_retries:
                    logger.warning(f"Download attempt {attempt} failed: {e}, retrying...")
                    if progress_cb:
                        progress_cb(f"Retrying download (attempt {attempt + 1})...", 0.0)
                    continue
                raise ConnectionError(f"Download failed after {max_retries} attempts: {e}") from e

        # Verify SHA-512 hash
        if expected_hash:
            if progress_cb:
                progress_cb("Verifying download integrity...", 0.62)

            if not self._verify_hash(installer_path, expected_hash):
                installer_path.unlink(missing_ok=True)
                raise RuntimeError(
                    "Download integrity check failed: SHA-512 hash mismatch.\n"
                    "The downloaded file may be corrupted or tampered with.\n"
                    "Please try again."
                )
        else:
            logger.warning(
                "SHA-512 checksum not available from Mozilla. "
                "Proceeding without integrity verification."
            )

        return installer_path

    def extract_installer(
        self,
        installer_path: Path,
        extract_dir: Path,
        progress_cb: Optional[Callable[[str, float], None]] = None,
        cancel_event: Optional[threading.Event] = None
    ) -> Path:
        """
        Extract Firefox files from the installer using its built-in /ExtractDir flag.

        The Firefox NSIS installer supports /ExtractDir=<path> which extracts
        all files without running the installer UI.

        Handles nested extraction (some versions extract into a subfolder) by
        moving contents up to the expected directory.

        Note: Cancellation during extraction is not possible because the
        subprocess blocks. The cancel_event is checked after extraction completes.

        Args:
            installer_path: Path to Firefox Setup exe
            extract_dir: Directory to extract into
            progress_cb: Optional progress callback
            cancel_event: Optional cancellation event (checked after extraction)

        Returns:
            Path to the directory containing firefox.exe

        Raises:
            RuntimeError: If extraction fails or firefox.exe not found
        """
        extract_dir.mkdir(parents=True, exist_ok=True)

        if progress_cb:
            progress_cb("Extracting Firefox files (this may take a moment)...", 0.65)

        logger.info(f"Extracting {installer_path} to {extract_dir}")

        try:
            result = subprocess.run(
                [str(installer_path), f"/ExtractDir={extract_dir}"],
                capture_output=True,
                timeout=300  # 5 minutes max
            )

            if result.returncode != 0:
                stderr = result.stderr.decode("utf-8", errors="replace") if result.stderr else ""
                raise RuntimeError(
                    f"Extraction failed (exit code {result.returncode}): {stderr}"
                )

        except subprocess.TimeoutExpired:
            raise RuntimeError("Extraction timed out after 5 minutes")

        # Check cancellation after extraction completes
        if cancel_event and cancel_event.is_set():
            shutil.rmtree(str(extract_dir), ignore_errors=True)
            raise RuntimeError("Update cancelled by user")

        # Handle nested extraction: some versions extract into a subfolder
        firefox_exe = extract_dir / "firefox.exe"
        if not firefox_exe.exists():
            for child in extract_dir.iterdir():
                if child.is_dir() and (child / "firefox.exe").exists():
                    # Move contents up one level via staging dir
                    staging = extract_dir.parent / f"{extract_dir.name}.staging"
                    try:
                        child.rename(staging)
                        shutil.rmtree(str(extract_dir))
                        staging.rename(extract_dir)
                    except OSError:
                        # Clean up staging on failure
                        if staging.exists():
                            shutil.rmtree(str(staging), ignore_errors=True)
                        raise
                    break

        firefox_exe = extract_dir / "firefox.exe"
        if not firefox_exe.exists():
            raise RuntimeError(
                f"Extraction completed but firefox.exe not found in {extract_dir}"
            )

        if progress_cb:
            progress_cb("Extraction complete", 0.75)

        logger.info(f"Extraction successful, firefox.exe at: {extract_dir}")
        return extract_dir
