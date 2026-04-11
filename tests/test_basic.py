import pytest
from typer.testing import CliRunner
from claudforge.cli import app

runner = CliRunner()

def test_help_command():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "Deploy a skill or a batch" in result.stdout

def test_doctor_command():
    result = runner.invoke(app, ["doctor"])
    assert result.exit_code == 0
    assert "Python Version" in result.stdout

def test_init_command(tmp_path):
    # Test scaffolding in a temporary directory
    with runner.isolated_filesystem(temp_dir=tmp_path):
        result = runner.invoke(app, ["init", "--name", "test-skill"])
        assert result.exit_code == 0
        assert "Created skill scaffold" in result.stdout
        assert (Path.cwd() / "test-skill" / "SKILL.md").exists()

from pathlib import Path
