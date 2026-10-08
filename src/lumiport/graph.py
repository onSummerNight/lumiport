from collections import defaultdict


def _resolve(target: str, by_path: dict, by_base: dict) -> str | None:
    hit = by_path.get(target.lower())
    if hit:
        return hit
    cands = by_base.get(target.rsplit("/", 1)[-1].lower(), [])
    return cands[0] if len(cands) == 1 else None


def _components(nodes: list, adj: dict) -> list:
    """Strongly connected components (iterative Tarjan)."""
    index, low, on, stack, out = {}, {}, set(), [], []
    for root in nodes:
        if root in index:
            continue
        index[root] = low[root] = len(index)
        stack.append(root)
        on.add(root)
        work = [(root, iter(adj[root]))]
        while work:
            node, it = work[-1]
            for nxt in it:
                if nxt not in index:
                    index[nxt] = low[nxt] = len(index)
                    stack.append(nxt)
                    on.add(nxt)
                    work.append((nxt, iter(adj[nxt])))
                    break
                if nxt in on:
                    low[node] = min(low[node], index[nxt])
            else:
                work.pop()
                if work:
                    parent = work[-1][0]
                    low[parent] = min(low[parent], low[node])
                if low[node] == index[node]:
                    comp = []
                    while True:
                        w = stack.pop()
                        on.discard(w)
                        comp.append(w)
                        if w == node:
                            break
                    out.append(sorted(comp))
    return out


def build_graph(files: list) -> dict:
    """Dependency graph of scanned files (see docs/SCHEMA.md)."""
    paths = sorted(f["path"] for f in files)
    by_path = {p.lower(): p for p in paths}
    by_base = defaultdict(list)
    for p in paths:
        by_base[p.rsplit("/", 1)[-1].lower()].append(p)

    edges, missing = set(), set()
    for f in files:
        for key, kind in (("runs", "run"), ("includes", "include")):
            for target in f[key]:
                dest = _resolve(target, by_path, by_base)
                if dest is None:
                    missing.add((f["path"], target))
                else:
                    edges.add((f["path"], dest, kind))

    out_edges = defaultdict(set)
    for a, b, _ in edges:
        out_edges[a].add(b)
    adj = {p: sorted(out_edges[p]) for p in paths}
    comps = _components(paths, adj)
    cycles = sorted(c for c in comps if len(c) > 1 or c[0] in adj[c[0]])

    comp_of = {p: i for i, c in enumerate(comps) for p in c}
    deps = [
        {comp_of[d] for p in c for d in adj[p]} - {i} for i, c in enumerate(comps)
    ]
    level: dict = {}

    def level_of(start: int) -> int:
        # components form a DAG; resolve depth without recursion
        todo = [start]
        while todo:
            i = todo[-1]
            pending = [d for d in deps[i] if d not in level]
            if pending:
                todo.extend(pending)
            else:
                level[i] = 1 + max((level[d] for d in deps[i]), default=0)
                todo.pop()
        return level[start]

    steps = defaultdict(list)
    for i, c in enumerate(comps):
        steps[level_of(i)].extend(c)

    return {
        "edges": [list(e) for e in sorted(edges)],
        "missing": [list(m) for m in sorted(missing)],
        "cycles": cycles,
        "order": [sorted(steps[n]) for n in sorted(steps)],
    }
