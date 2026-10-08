from lumiport.metrics import file_metrics
from lumiport.tokenizer import strip_code


def metrics(src: str) -> dict:
    return file_metrics(strip_code(src))


def test_blank_lines_only():
    assert metrics("\n   \n\t\n") == {"loc": 0, "blocks": 0, "branches": 0}


def test_end_error_not_counted():
    m = metrics("DO ON ERROR UNDO:\n  RUN x.\nEND.\nCATCH e AS Progress.Lang.Error:\nEND-ERROR.\nEND-KEY.")
    assert m["blocks"] == 1


def test_lower_case_if():
    assert metrics("if x then y = 1.")["branches"] == 1


def test_case_when_counts_each_when():
    m = metrics("CASE x:\n  WHEN 1 THEN y = 1.\n  WHEN 2 THEN y = 2.\nEND CASE.")
    assert (m["branches"], m["blocks"]) == (2, 1)


def test_comment_only_line_is_not_loc():
    assert metrics("/* just a note */\nx = 1.\n")["loc"] == 1


def test_self_call_adds_no_fan(tmp_path):
    from lumiport.scanner import scan_dir

    (tmp_path / "s.p").write_text("RUN s.p.\n")
    m = scan_dir(tmp_path)["files"][0]["metrics"]
    assert (m["fan_in"], m["fan_out"], m["score"]) == (0, 0, 1)
