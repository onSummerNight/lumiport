from lumiport.graph import build_graph


def f(path, runs=(), includes=()):
    return {"path": path, "runs": list(runs), "includes": list(includes)}


def test_self_call():
    g = build_graph([f("a.p", runs=["a.p"])])
    assert g["cycles"] == [["a.p"]]
    assert g["order"] == [["a.p"]]


def test_missing_target():
    g = build_graph([f("a.p", runs=["gone.p"])])
    assert g["missing"] == [["a.p", "gone.p"]]
    assert g["edges"] == []


def test_diamond():
    g = build_graph([
        f("top.p", runs=["l.p", "r.p"]),
        f("l.p", runs=["base.p"]),
        f("r.p", runs=["base.p"]),
        f("base.p"),
    ])
    assert g["cycles"] == []
    assert g["order"] == [["base.p"], ["l.p", "r.p"], ["top.p"]]


def test_basename_and_case_resolution():
    g = build_graph([f("a.p", runs=["B.P", "util.i"]), f("sub/b.p"), f("sub/util.i")])
    assert g["edges"] == [["a.p", "sub/b.p", "run"], ["a.p", "sub/util.i", "run"]]
    assert g["missing"] == []


def test_ambiguous_basename_is_missing():
    g = build_graph([f("a.p", runs=["x.p"]), f("one/x.p"), f("two/x.p")])
    assert g["missing"] == [["a.p", "x.p"]]


def test_three_file_cycle():
    g = build_graph([
        f("a.p", runs=["b.p"]),
        f("b.p", runs=["c.p"]),
        f("c.p", runs=["a.p"]),
        f("d.p", runs=["a.p"]),
    ])
    assert g["cycles"] == [["a.p", "b.p", "c.p"]]
    assert g["order"] == [["a.p", "b.p", "c.p"], ["d.p"]]
