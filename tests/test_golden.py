import json
from pathlib import Path

from typer.testing import CliRunner

from lumiport.cli import app
from lumiport.scanner import scan_dir

SAMPLES = Path(__file__).resolve().parent.parent / "samples"


def test_scan_matches_expected():
    expected = json.loads((SAMPLES / "expected.json").read_text())
    assert scan_dir(SAMPLES / "app") == expected


def test_cli_out_matches_expected(tmp_path):
    out = tmp_path / "tmp.json"
    result = CliRunner().invoke(app, ["scan", str(SAMPLES / "app"), "--out", str(out)])
    assert result.exit_code == 0
    assert json.loads(out.read_text()) == json.loads((SAMPLES / "expected.json").read_text())
