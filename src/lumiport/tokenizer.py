def strip_code(text: str) -> str:
    """Blank comments and string literals with spaces, keeping newlines."""
    out = []
    n = len(text)
    i = 0
    depth = 0  # comment nesting
    quote = ""  # active string delimiter, or ""

    def blank(ch: str) -> str:
        return ch if ch in "\r\n" else " "

    while i < n:
        ch = text[i]
        two = text[i : i + 2]
        if depth:
            if two == "/*":
                depth += 1
            elif two == "*/":
                depth -= 1
            else:
                out.append(blank(ch))
                i += 1
                continue
            out.append("  ")
            i += 2
        elif quote:
            if ch == "~" and i + 1 < n:
                out.append(blank(ch) + blank(text[i + 1]))
                i += 2
                continue
            if ch == quote:
                if text[i + 1 : i + 2] == quote:  # doubled quote stays inside
                    out.append("  ")
                    i += 2
                    continue
                quote = ""
            out.append(blank(ch))
            i += 1
        elif two == "/*":
            depth = 1
            out.append("  ")
            i += 2
        elif ch in "\"'":
            quote = ch
            out.append(" ")
            i += 1
        else:
            out.append(ch)
            i += 1
    return "".join(out)
