import json
from pathlib import Path

from typer.testing import CliRunner

from lumiport.cli import app
from lumiport.report import render_report

SAMPLES = Path(__file__).resolve().parent.parent / "samples"


def test_report_matches_expected():
    inventory = json.loads((SAMPLES / "expected.json").read_text())
    assert render_report(inventory) == (SAMPLES / "expected-report.md").read_text()


def test_empty_inventory_renders_none():
    text = render_report({"files": [], "graph": {"edges": [], "missing": [], "cycles": [], "order": []}})
    for heading in ("Migration order", "Cycles", "Missing targets", "Unresolved dynamic calls", "Tables", "Files"):
        assert f"## {heading}\n\nNone" in text


def test_cli_report_writes_file(tmp_path):
    out = tmp_path / "r.md"
    result = CliRunner().invoke(app, ["scan", str(SAMPLES / "app"), "--report", str(out)])
    assert result.exit_code == 0
    assert out.read_text() == (SAMPLES / "expected-report.md").read_text()


def test_report_groups_table_case_across_files():
    def f(path, tables):
        return {"path": path, "kind": "p", "units": [], "includes": [], "runs": [], "unresolved_runs": 0,
                "tables": tables, "metrics": {"loc": 1, "blocks": 0, "branches": 0, "fan_in": 0, "fan_out": 0, "score": 1}}

    inv = {"files": [f("a.p", {"Customer": "read"}), f("b.p", {"customer": "write"})],
           "graph": {"edges": [], "missing": [], "cycles": [], "order": [["a.p", "b.p"]]}}
    text = render_report(inv)
    assert "- Tables: 1" in text
    assert "| Customer | a.p | b.p |" in text
