import importlib.util
from pathlib import Path

MODULE_PATH = Path(__file__).resolve().parents[1] / "bash2ps.py"
spec = importlib.util.spec_from_file_location("bash2ps", MODULE_PATH)
bash2ps = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bash2ps)


def test_translate_ls_la_returns_powershell_suggestion():
    suggestions = bash2ps.translate_command("ls -la")
    assert suggestions
    assert any("Get-ChildItem" in suggestion for suggestion in suggestions)


def test_translate_pwd_returns_get_location():
    suggestions = bash2ps.translate_command("pwd")
    assert suggestions
    assert any("Get-Location" in suggestion for suggestion in suggestions)


def test_translate_which_returns_get_command():
    suggestions = bash2ps.translate_command("which python")
    assert suggestions
    assert any("Get-Command" in suggestion for suggestion in suggestions)


def test_tutorial_contains_intro_and_commands():
    tutorial = bash2ps.build_tutorial_text()
    assert "5-minute" in tutorial
    assert "Get-ChildItem" in tutorial
    assert "PowerShell" in tutorial
