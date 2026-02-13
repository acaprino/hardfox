#!/usr/bin/env python3
"""
Integration tests for the BASE/ADVANCED settings separation.

Verifies:
- BASE settings → prefs.js with pref() syntax
- ADVANCED settings → user.js with user_pref() syntax
- Merge behavior for prefs.js
- File creation when prefs.js doesn't exist
- Firefox-running check
- Atomic write safety
"""

import pytest
from pathlib import Path
from unittest.mock import patch

from hardfox.domain.entities.setting import Setting
from hardfox.domain.enums import SettingLevel, SettingType
from hardfox.infrastructure.parsers import PrefsParser
from hardfox.infrastructure.persistence.firefox_file_repository import FirefoxFileRepository
from hardfox.application.use_cases.apply_settings_use_case import ApplySettingsUseCase
from hardfox.application.mappers import SettingToPrefMapper


@pytest.fixture
def temp_profile(tmp_path):
    """Create a minimal Firefox profile directory."""
    # Create prefs.js marker so validate_profile_path passes
    (tmp_path / "prefs.js").write_text(
        'pref("existing.pref", true);\n', encoding='utf-8'
    )
    return tmp_path


@pytest.fixture
def parser():
    return PrefsParser()


@pytest.fixture
def repo(parser):
    return FirefoxFileRepository(parser)


@pytest.fixture
def use_case(repo):
    return ApplySettingsUseCase(repo, SettingToPrefMapper())


def _make_setting(key, value, level, setting_type=SettingType.TOGGLE):
    """Helper to create a Setting with minimal required fields."""
    kwargs = dict(
        key=key,
        value=value,
        level=level,
        setting_type=setting_type,
        category="test",
    )
    if setting_type == SettingType.SLIDER:
        kwargs.update(min_value=0, max_value=100, step=1)
    return Setting(**kwargs)


# ── SettingLevel enum tests ──────────────────────────────────────────────

class TestSettingLevelEnum:
    def test_base_filename_is_prefs_js(self):
        assert SettingLevel.BASE.filename == "prefs.js"

    def test_advanced_filename_is_user_js(self):
        assert SettingLevel.ADVANCED.filename == "user.js"

    def test_base_prefix_is_pref(self):
        assert SettingLevel.BASE.prefix == "pref"

    def test_advanced_prefix_is_user_pref(self):
        assert SettingLevel.ADVANCED.prefix == "user_pref"


# ── Setting.to_firefox_pref tests ────────────────────────────────────────

class TestSettingToFirefoxPref:
    def test_base_setting_uses_pref_prefix(self):
        s = _make_setting("test.base", True, SettingLevel.BASE)
        assert s.to_firefox_pref() == 'pref("test.base", true);'

    def test_advanced_setting_uses_user_pref_prefix(self):
        s = _make_setting("test.advanced", True, SettingLevel.ADVANCED)
        assert s.to_firefox_pref() == 'user_pref("test.advanced", true);'


# ── Repository write tests ──────────────────────────────────────────────

class TestRepositoryWriteLevel:
    @patch.object(FirefoxFileRepository, 'is_firefox_running', return_value=False)
    def test_write_base_creates_prefs_js_with_user_pref_syntax(self, _mock, temp_profile, repo):
        repo.write_prefs(temp_profile, {"test.key": True}, SettingLevel.BASE)
        content = (temp_profile / "prefs.js").read_text(encoding='utf-8')
        assert 'user_pref("test.key", true);' in content

    @patch.object(FirefoxFileRepository, 'is_firefox_running', return_value=False)
    def test_write_advanced_creates_user_js_with_user_pref_syntax(self, _mock, temp_profile, repo):
        repo.write_prefs(temp_profile, {"test.key": 42}, SettingLevel.ADVANCED)
        content = (temp_profile / "user.js").read_text(encoding='utf-8')
        assert 'user_pref("test.key", 42);' in content

    @patch.object(FirefoxFileRepository, 'is_firefox_running', return_value=False)
    def test_write_base_merges_with_existing(self, _mock, temp_profile, repo):
        repo.write_prefs(temp_profile, {"new.pref": "hello"}, SettingLevel.BASE, merge=True)
        content = (temp_profile / "prefs.js").read_text(encoding='utf-8')
        # Existing pref should be merged in
        assert 'user_pref("existing.pref", true);' in content
        assert 'user_pref("new.pref", "hello");' in content

    @patch.object(FirefoxFileRepository, 'is_firefox_running', return_value=False)
    def test_write_base_creates_prefs_js_when_missing(self, _mock, tmp_path, repo):
        """Test prefs.js creation when profile only has times.json."""
        (tmp_path / "times.json").write_text("{}", encoding='utf-8')
        # prefs.js doesn't exist, but times.json validates the profile
        repo.write_prefs(tmp_path, {"test": False}, SettingLevel.BASE, merge=True)
        assert (tmp_path / "prefs.js").exists()
        content = (tmp_path / "prefs.js").read_text(encoding='utf-8')
        assert 'user_pref("test", false);' in content


# ── Firefox-running check tests ─────────────────────────────────────────

class TestFirefoxRunningCheck:
    @patch.object(FirefoxFileRepository, 'is_firefox_running', return_value=True)
    def test_write_raises_when_firefox_running(self, _mock, temp_profile, repo):
        with pytest.raises(RuntimeError, match="Firefox is running"):
            repo.write_prefs(temp_profile, {"test": True}, SettingLevel.BASE)

    @patch.object(FirefoxFileRepository, 'is_firefox_running', return_value=True)
    def test_write_advanced_also_blocked_when_firefox_running(self, _mock, temp_profile, repo):
        with pytest.raises(RuntimeError, match="Firefox is running"):
            repo.write_prefs(temp_profile, {"test": True}, SettingLevel.ADVANCED)

    @patch.object(FirefoxFileRepository, 'is_firefox_running', return_value=False)
    def test_write_succeeds_when_firefox_not_running(self, _mock, temp_profile, repo):
        repo.write_prefs(temp_profile, {"test": True}, SettingLevel.ADVANCED)
        assert (temp_profile / "user.js").exists()


# ── End-to-end ApplySettingsUseCase tests ────────────────────────────────

class TestApplySettingsUseCase:
    @patch.object(FirefoxFileRepository, 'is_firefox_running', return_value=False)
    def test_treats_all_settings_as_base_and_clears_user_js(self, _mock, temp_profile, use_case):
        settings = {
            "base.toggle": _make_setting("base.toggle", True, SettingLevel.BASE),
            "adv.toggle": _make_setting("adv.toggle", False, SettingLevel.ADVANCED),
        }

        result = use_case.execute(temp_profile, settings)

        # Everything is treated as BASE
        assert result["base_applied"] == 2
        assert result["advanced_applied"] == 0

        prefs_content = (temp_profile / "prefs.js").read_text(encoding='utf-8')
        user_content = (temp_profile / "user.js").read_text(encoding='utf-8')

        # ALL settings in prefs.js with user_pref()
        assert 'user_pref("base.toggle", true);' in prefs_content
        assert 'user_pref("adv.toggle", false);' in prefs_content

        # user.js should be effectively empty (cleared)
        # It might contain the header, but no content
        assert "user_pref" not in user_content

    @patch.object(FirefoxFileRepository, 'is_firefox_running', return_value=False)
    def test_always_clears_user_js(self, _mock, temp_profile, use_case):
        # Create a pre-existing user.js with locked settings
        (temp_profile / "user.js").write_text('user_pref("locked.pref", true);', encoding='utf-8')

        # Apply only a base setting
        settings = {
            "base.s": _make_setting("base.s", True, SettingLevel.BASE),
        }
        
        use_case.execute(temp_profile, settings)

        # user.js should have been overwritten/cleared
        user_content = (temp_profile / "user.js").read_text(encoding='utf-8')
        assert "locked.pref" not in user_content
        assert "user_pref" not in user_content

    @patch.object(FirefoxFileRepository, 'is_firefox_running', return_value=False)
    def test_empty_settings_returns_zero(self, _mock, temp_profile, use_case):
        result = use_case.execute(temp_profile, {})
        assert result == {"base_applied": 0, "advanced_applied": 0}

    @patch.object(FirefoxFileRepository, 'is_firefox_running', return_value=True)
    def test_raises_when_firefox_running(self, _mock, temp_profile, use_case):
        settings = {
            "s": _make_setting("s", True, SettingLevel.BASE),
        }
        with pytest.raises(RuntimeError, match="Firefox is running"):
            use_case.execute(temp_profile, settings)


# ── Atomic write tests ──────────────────────────────────────────────────

class TestAtomicWrite:
    def test_write_includes_timestamp_header(self, tmp_path, parser):
        out = tmp_path / "test.js"
        parser.write_prefs({"key": True}, out)
        content = out.read_text(encoding='utf-8')
        assert "Hardfox Firefox Configuration - Generated 20" in content

    def test_write_produces_valid_parseable_output(self, tmp_path, parser):
        out = tmp_path / "test.js"
        prefs = {"a.bool": True, "b.int": 42, "c.str": "hello"}
        parser.write_prefs(prefs, out)
        parsed = parser.parse_file(out)
        assert parsed == prefs

    def test_no_temp_files_left_on_success(self, tmp_path, parser):
        out = tmp_path / "test.js"
        parser.write_prefs({"k": 1}, out)
        tmp_files = list(tmp_path.glob("*.tmp"))
        assert len(tmp_files) == 0


# ── Sync Protection tests ─────────────────────────────────────────────

class TestSyncProtection:
    @patch.object(FirefoxFileRepository, 'is_firefox_running', return_value=False)
    def test_sync_protection_disabled_no_sync_prefs_generated(self, _mock, temp_profile, use_case):
        """When sync protection is OFF, no services.sync.prefs.sync.* prefs are auto-generated."""
        settings = {
            "hardfox.sync_protection.enabled": _make_setting(
                "hardfox.sync_protection.enabled", False, SettingLevel.BASE
            ),
            "privacy.trackingprotection.enabled": _make_setting(
                "privacy.trackingprotection.enabled", True, SettingLevel.BASE
            ),
        }
        use_case.execute(temp_profile, settings)
        content = (temp_profile / "prefs.js").read_text(encoding='utf-8')
        assert 'user_pref("privacy.trackingprotection.enabled", true);' in content
        assert 'services.sync.prefs.sync' not in content

    @patch.object(FirefoxFileRepository, 'is_firefox_running', return_value=False)
    def test_sync_protection_enabled_generates_sync_prefs(self, _mock, temp_profile, use_case):
        """When sync protection is ON, auto-generates services.sync.prefs.sync.<key> = false."""
        settings = {
            "hardfox.sync_protection.enabled": _make_setting(
                "hardfox.sync_protection.enabled", True, SettingLevel.BASE
            ),
            "privacy.trackingprotection.enabled": _make_setting(
                "privacy.trackingprotection.enabled", True, SettingLevel.BASE
            ),
            "dom.battery.enabled": _make_setting(
                "dom.battery.enabled", False, SettingLevel.BASE
            ),
        }
        use_case.execute(temp_profile, settings)
        content = (temp_profile / "prefs.js").read_text(encoding='utf-8')
        # Original settings written
        assert 'user_pref("privacy.trackingprotection.enabled", true);' in content
        assert 'user_pref("dom.battery.enabled", false);' in content
        # Sync protection prefs auto-generated
        assert 'user_pref("services.sync.prefs.sync.privacy.trackingprotection.enabled", false);' in content
        assert 'user_pref("services.sync.prefs.sync.dom.battery.enabled", false);' in content

    @patch.object(FirefoxFileRepository, 'is_firefox_running', return_value=False)
    def test_sync_protection_does_not_generate_nested_keys(self, _mock, temp_profile, use_case):
        """Sync settings (services.sync.*) must NOT get nested sync protection keys."""
        settings = {
            "hardfox.sync_protection.enabled": _make_setting(
                "hardfox.sync_protection.enabled", True, SettingLevel.BASE
            ),
            "services.sync.engine.passwords": _make_setting(
                "services.sync.engine.passwords", False, SettingLevel.BASE
            ),
            "privacy.resistFingerprinting": _make_setting(
                "privacy.resistFingerprinting", False, SettingLevel.BASE
            ),
        }
        use_case.execute(temp_profile, settings)
        content = (temp_profile / "prefs.js").read_text(encoding='utf-8')
        # Sync engine setting written directly
        assert 'user_pref("services.sync.engine.passwords", false);' in content
        # Regular setting gets sync protection
        assert 'user_pref("services.sync.prefs.sync.privacy.resistFingerprinting", false);' in content
        # No nested nonsense like services.sync.prefs.sync.services.sync.*
        assert 'services.sync.prefs.sync.services.sync' not in content

    @patch.object(FirefoxFileRepository, 'is_firefox_running', return_value=False)
    def test_explicit_sync_override_preserved(self, _mock, temp_profile, use_case):
        """User's explicit sync control settings override auto-generated sync protection."""
        settings = {
            "hardfox.sync_protection.enabled": _make_setting(
                "hardfox.sync_protection.enabled", True, SettingLevel.BASE
            ),
            # User explicitly wants cookie behavior to sync (True)
            "services.sync.prefs.sync.network.cookie.cookieBehavior": _make_setting(
                "services.sync.prefs.sync.network.cookie.cookieBehavior", True, SettingLevel.BASE
            ),
            # This is the regular setting that would normally get sync protection
            "network.cookie.cookieBehavior": _make_setting(
                "network.cookie.cookieBehavior", 4, SettingLevel.BASE,
                setting_type=SettingType.SLIDER
            ),
        }
        use_case.execute(temp_profile, settings)
        content = (temp_profile / "prefs.js").read_text(encoding='utf-8')
        # User's explicit sync=true is preserved, NOT overwritten to false
        assert 'user_pref("services.sync.prefs.sync.network.cookie.cookieBehavior", true);' in content
        # Verify no duplicate false entry
        assert content.count('services.sync.prefs.sync.network.cookie.cookieBehavior') == 1

    @patch.object(FirefoxFileRepository, 'is_firefox_running', return_value=False)
    def test_hardfox_internal_flags_never_written(self, _mock, temp_profile, use_case):
        """Internal hardfox.* flags must never appear in Firefox prefs files."""
        settings = {
            "hardfox.sync_protection.enabled": _make_setting(
                "hardfox.sync_protection.enabled", True, SettingLevel.BASE
            ),
            "browser.send_pings": _make_setting(
                "browser.send_pings", False, SettingLevel.BASE
            ),
        }
        use_case.execute(temp_profile, settings)
        content = (temp_profile / "prefs.js").read_text(encoding='utf-8')
        assert 'hardfox.' not in content

    @patch.object(FirefoxFileRepository, 'is_firefox_running', return_value=False)
    def test_sync_protection_count_includes_generated_prefs(self, _mock, temp_profile, use_case):
        """Return count should include auto-generated sync protection prefs."""
        settings = {
            "hardfox.sync_protection.enabled": _make_setting(
                "hardfox.sync_protection.enabled", True, SettingLevel.BASE
            ),
            "privacy.donottrackheader.enabled": _make_setting(
                "privacy.donottrackheader.enabled", False, SettingLevel.BASE
            ),
            "browser.send_pings": _make_setting(
                "browser.send_pings", False, SettingLevel.BASE
            ),
        }
        result = use_case.execute(temp_profile, settings)
        # 2 regular settings + 2 auto-generated sync prefs = 4
        assert result["base_applied"] == 4
