import json
from pathlib import Path

import pytest

from lumiport.extract import extract_calls, extract_tables
from lumiport.tokenizer import strip_code

SAMPLES = Path(__file__).resolve().parent.parent / "samples"
EXPECTED = json.loads((SAMPLES / "expected.json").read_text())["files"]
FIELDS = ("units", "includes", "runs", "unresolved_runs")


@pytest.mark.parametrize("entry", EXPECTED, ids=lambda e: e["path"])
def test_sample_file(entry):
    code = strip_code((SAMPLES / "app" / entry["path"]).read_text())
    got = extract_calls(code)
    assert got == {k: entry[k] for k in FIELDS}


def test_lower_case_keywords():
    got = extract_calls("procedure foo:\nend procedure.\nrun a.p.\nrun value(x).\n")
    assert got["units"] == [{"name": "foo", "type": "procedure"}]
    assert got["runs"] == ["a.p"] and got["unresolved_runs"] == 1


def test_forward_function_is_not_a_unit():
    code = "FUNCTION f RETURNS INTEGER (INPUT x AS INTEGER) FORWARD.\n"
    assert extract_calls(code)["units"] == []


def test_forward_then_definition_counts_once():
    code = (
        "FUNCTION f RETURNS INTEGER () FORWARD.\n"
        "FUNCTION f RETURNS INTEGER ():\nRETURN 1.\nEND FUNCTION.\n"
    )
    assert extract_calls(code)["units"] == [{"name": "f", "type": "function"}]


def test_preprocessor_reference_is_not_an_include():
    got = extract_calls("{&X}\n{}\n{inc.i &A=1}\n")
    assert got["includes"] == ["inc.i"]


def test_run_persistent_and_path():
    got = extract_calls("RUN dir/x.p PERSISTENT SET h.\nRUN x.p.\nRUN local.\n")
    assert got["runs"] == ["dir/x.p", "x.p"]


def test_dynamic_function_is_not_a_unit():
    assert extract_calls("x = DYNAMIC-FUNCTION(h).")["units"] == []


@pytest.mark.parametrize("entry", EXPECTED, ids=lambda e: e["path"])
def test_sample_tables(entry):
    code = strip_code((SAMPLES / "app" / entry["path"]).read_text())
    assert extract_tables(code) == entry["tables"]


def test_tables_lower_case_keywords():
    code = "for each customer:\nend.\nfind first order.\ncreate item.\ndelete item.\n"
    assert extract_tables(code) == {"customer": "read", "item": "write", "order": "read"}


def test_tables_join_parts():
    code = "FOR EACH a, EACH b WHERE b.x = a.x:\nEND.\n"
    assert extract_tables(code) == {"a": "read", "b": "read"}


def test_buffer_used_before_definition():
    code = (
        "FIND FIRST bo.\nCREATE BO.\n"
        "DEFINE BUFFER bo FOR order.\n"
    )
    assert extract_tables(code) == {"order": "write"}


def test_dynamic_create_and_delete_are_not_tables():
    code = "CREATE QUERY hQ.\nDELETE OBJECT h.\nCREATE BUFFER hB FOR TABLE x.\n"
    assert extract_tables(code) == {}


def test_find_current_with_lock():
    assert extract_tables("FIND CURRENT x EXCLUSIVE-LOCK.\n") == {"x": "read"}


def test_field_references_are_not_access():
    code = "FOR EACH order-line WHERE order-line.order-num = order.num:\nEND.\n"
    assert extract_tables(code) == {"order-line": "read"}


def test_private_procedure():
    got = extract_calls("PROCEDURE p PRIVATE:\nEND PROCEDURE.\n")
    assert got["units"] == [{"name": "p", "type": "procedure"}]


def test_lower_case_private_procedure():
    got = extract_calls("procedure p private:\nend procedure.\n")
    assert got["units"] == [{"name": "p", "type": "procedure"}]


def test_end_procedure_is_not_a_unit():
    assert extract_calls("END PROCEDURE.\n")["units"] == []
