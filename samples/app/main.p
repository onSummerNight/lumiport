/* main.p - entry point */
{common.i}
{consts.i}

DEFINE VARIABLE cProg AS CHARACTER NO-UNDO.

cProg = "report.p".

RUN a.p.
RUN VALUE(cProg).

FOR EACH customer NO-LOCK:
    gcStatus = customer.name.
END.
