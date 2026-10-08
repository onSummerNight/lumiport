import json
from pathlib import Path

import pytest

SAMPLES = Path(__file__).resolve().parent.parent / "samples"


@pytest.mark.xfail(strict=True, reason="scanner not built")
def test_scan_matches_expected():
    from lumiport.scanner import scan_dir  # does not exist yet

    expected = json.loads((SAMPLES / "expected.json").read_text())
    assert scan_dir(SAMPLES / "app") == expected
