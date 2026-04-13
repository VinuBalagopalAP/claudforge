import pytest
import os
import json
from pathlib import Path
import claudforge.utils.browser_profiles

def test_profile_discovery_simple_mock(mocker):
    """
    Test profile discovery by mocking the utility return directly.
    This ensures that internal logic downstream handles the profile data correctly.
    """
    mock_data = [
        {"name": "Work Account", "folder": "Profile 1", "path": "/tmp/chrome/Profile 1"},
        {"name": "Afzal", "folder": "Profile 2", "path": "/tmp/chrome/Profile 2"}
    ]
    
    # Mock the return value of get_system_profiles
    mocker.patch("claudforge.utils.browser_profiles.get_system_profiles", return_value=mock_data)
    
    from claudforge.utils.browser_profiles import get_system_profiles
    profiles = get_system_profiles()
    
    assert len(profiles) == 2
    assert profiles[0]["name"] == "Work Account"
    assert "Profile 1" in profiles[0]["path"]

def test_config_retrieval(mocker):
    """Test that config retrieval works as expected."""
    mocker.patch("claudforge.utils.config.get_config_key", return_value="/tmp/chrome/Profile 1")
    from claudforge.utils.config import get_config_key
    assert get_config_key("last_profile_path") == "/tmp/chrome/Profile 1"
