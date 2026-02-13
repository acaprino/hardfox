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
    def test_write_base_creates_prefs_js_with_pref_syntax(self, _mock, temp_profile, repo):
        repo.write_prefs(temp_profile, {"test.key": True}, SettingLevel.BASE)
        content = (temp_profile / "prefs.js").read_text(encoding='utf-8')
        assert 'pref("test.key", true);' in content
        assert 'user_pref' not in content

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
        assert 'pref("existing.pref", true);' in content
        assert 'pref("new.pref", "hello");' in content

    @patch.object(FirefoxFileRepository, 'is_firefox_running', return_value=False)
    def test_write_base_creates_prefs_js_when_missing(self, _mock, tmp_path, repo):
        """Test prefs.js creation when profile only has times.json."""
        (tmp_path / "times.json").write_text("{}", encoding='utf-8')
        # prefs.js doesn't exist, but times.json validates the profile
        repo.write_prefs(tmp_path, {"test": False}, SettingLevel.BASE, merge=True)
        assert (tmp_path / "prefs.js").exists()
        content = (tmp_path / "prefs.js").read_text(encoding='utf-8')
        assert 'pref("test", false);' in content


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
    def test_separates_base_and_advanced_into_different_files(self, _mock, temp_profile, use_case):
        settings = {
            "base.toggle": _make_setting("base.toggle", True, SettingLevel.BASE),
            "adv.toggle": _make_setting("adv.toggle", False, SettingLevel.ADVANCED),
        }

        result = use_case.execute(temp_profile, settings)

        assert result["base_applied"] == 1
        assert result["advanced_applied"] == 1

        prefs_content = (temp_profile / "prefs.js").read_text(encoding='utf-8')
        user_content = (temp_profile / "user.js").read_text(encoding='utf-8')

        # BASE in prefs.js with pref()
        assert 'pref("base.toggle", true);' in prefs_content
        # ADVANCED in user.js with user_pref()
        assert 'user_pref("adv.toggle", false);' in user_content
        # No cross-contamination
        assert "adv.toggle" not in prefs_content
        assert "base.toggle" not in user_content

    @patch.object(FirefoxFileRepository, 'is_firefox_running', return_value=False)
    def test_apply_only_base(self, _mock, temp_profile, use_case):
        settings = {
            "base.s": _make_setting("base.s", True, SettingLevel.BASE),
            "adv.s": _make_setting("adv.s", True, SettingLevel.ADVANCED),
        }
        result = use_case.execute(temp_profile, settings, level=SettingLevel.BASE)
        assert result["base_applied"] == 1
        assert result["advanced_applied"] == 0
        assert not (temp_profile / "user.js").exists()

    @patch.object(FirefoxFileRepository, 'is_firefox_running', return_value=False)
    def test_apply_only_advanced(self, _mock, temp_profile, use_case):
        settings = {
            "base.s": _make_setting("base.s", True, SettingLevel.BASE),
            "adv.s": _make_setting("adv.s", True, SettingLevel.ADVANCED),
        }
        result = use_case.execute(temp_profile, settings, level=SettingLevel.ADVANCED)
        assert result["base_applied"] == 0
        assert result["advanced_applied"] == 1

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
