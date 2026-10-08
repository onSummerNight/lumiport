/* a.p - first half of the cycle */
{common.i}

giDepth = giDepth + 1.
IF giDepth < 3 THEN RUN b.p.

FIND FIRST order NO-LOCK WHERE order.status = "open" NO-ERROR.
