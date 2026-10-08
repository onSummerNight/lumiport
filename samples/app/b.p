/* b.p - second half of the cycle */
{common.i}

giDepth = giDepth + 1.
IF giDepth < 3 THEN RUN a.p.

FOR EACH order-line NO-LOCK:
    gcStatus = order-line.item-code.
END.
