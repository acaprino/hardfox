#!/usr/bin/env python3
"""
Import Firefox Profile → Hardfox JSON

Reads a Firefox profile's user.js, maps known settings to Hardfox format,
and saves as a JSON profile in the profiles/ directory.

Usage:
    python import_profile.py [PROFILE_PATH] [--name NAME]

Examples:
    python import_profile.py "C:\\Users\\alfio\\Desktop\\MyFox\\Data\\profile" --name MyFox
    python import_profile.py  # uses defaults
"""

import argparse
import logging
import sys
from pathlib import Path

# Ensure project root is on sys.path for imports
sys.path.insert(0, str(Path(__file__).parent))

from hardfox.infrastructure.persistence.metadata_settings_repository import MetadataSettingsRepository
from hardfox.infrastructure.persistence.firefox_file_repository import FirefoxFileRepository
from hardfox.infrastructure.persistence.json_profile_repository import JsonProfileRepository
from hardfox.application.mappers.pref_to_setting_mapper import PrefToSettingMapper
from hardfox.application.use_cases.import_from_firefox_use_case import ImportFromFirefoxUseCase
from hardfox.application.use_cases.save_profile_use_case import SaveProfileUseCase


DEFAULT_PROFILE_PATH = r"C:\Users\alfio\Desktop\MyFox\Data\profile"
DEFAULT_NAME = "MyFox"


def main():
    parser = argparse.ArgumentParser(
        description="Import a Firefox profile into a Hardfox JSON profile."
    )
    parser.add_argument(
        "profile_path",
        nargs="?",
        default=DEFAULT_PROFILE_PATH,
        help=f"Path to Firefox profile directory (default: {DEFAULT_PROFILE_PATH})",
    )
    parser.add_argument(
        "--name",
        default=DEFAULT_NAME,
        help=f"Name for the imported profile (default: {DEFAULT_NAME})",
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose logging",
    )
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(levelname)s: %(message)s",
    )

    profile_path = Path(args.profile_path)
    profiles_dir = Path(__file__).parent / "profiles"

    # Wire up components
    settings_repo = MetadataSettingsRepository()
    firefox_repo = FirefoxFileRepository()
    mapper = PrefToSettingMapper(settings_repo)
    import_uc = ImportFromFirefoxUseCase(firefox_repo, mapper)
    profile_repo = JsonProfileRepository(profiles_dir, settings_repo)
    save_uc = SaveProfileUseCase(profile_repo)

    # Import and save
    print(f"Importing from: {profile_path}")
    profile = import_uc.execute(profile_path, profile_name=args.name)
    save_uc.execute(profile)

    output_file = profiles_dir / f"{args.name.lower().replace(' ', '_')}.json"
    print(f"Saved {len(profile.settings)} settings to {output_file}")


if __name__ == "__main__":
    main()
