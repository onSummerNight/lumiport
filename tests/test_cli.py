import json

from typer.testing import CliRunner

from lumiport.cli import app

runner = CliRunner()


def test_scan_existing_dir(tmp_path):
    result = runner.invoke(app, ["scan", str(tmp_path)])
    assert result.exit_code == 0
    assert json.loads(result.output) == {"files": []}


def test_scan_missing_dir(tmp_path):
    result = runner.invoke(app, ["scan", str(tmp_path / "missing")])
    assert result.exit_code != 0
