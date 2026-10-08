from pathlib import Path

from lumiport.tokenizer import strip_code

APP = Path(__file__).resolve().parent.parent / "samples" / "app"


def test_plain_code_unchanged():
    assert strip_code("RUN a.p.\n{x.i}") == "RUN a.p.\n{x.i}"


def test_comment_blanked():
    assert strip_code("a /* RUN x.p */ b") == "a" + " " * 14 + " b"


def test_comment_nests():
    out = strip_code("a /* o /* i */ still */ b")
    assert out.split() == ["a", "b"]


def test_string_blanked_both_quotes():
    assert strip_code("x \"RUN a.p\" 'FIND t' y").split() == ["x", "y"]


def test_tilde_escapes_next_char():
    assert strip_code('"a~"RUN b.p" z').split() == ["z"]


def test_doubled_quote_stays_in_string():
    assert strip_code("\"a\"\"RUN b.p\" z").split() == ["z"]
    assert strip_code("'a''RUN b.p' z").split() == ["z"]


def test_comment_marker_in_string_is_text():
    assert strip_code('"/*" RUN a.p.').split() == ["RUN", "a.p."]


def test_quote_in_comment_is_text():
    assert strip_code("/* it's */ RUN a.p.").split() == ["RUN", "a.p."]


def test_unterminated_comment_blanks_to_end():
    assert strip_code("a /* b\nc").split() == ["a"]


def test_unterminated_string_blanks_to_end():
    assert strip_code('a "b\nc').split() == ["a"]


def test_newlines_kept():
    src = '/* a\nb */\n"x\ny"\nz'
    out = strip_code(src)
    assert out.count("\n") == src.count("\n") and len(out) == len(src)


def test_report_decoys_removed():
    out = strip_code((APP / "report.p").read_text())
    for gone in ("ghost", "phantom", "fake.p", "decoy", "ghost-row"):
        assert gone not in out
    assert "printLine" in out and "FOR EACH order" in out


def test_length_and_newlines_preserved_on_samples():
    for f in APP.iterdir():
        src = f.read_text()
        out = strip_code(src)
        assert len(out) == len(src), f.name
        assert out.count("\n") == src.count("\n"), f.name
