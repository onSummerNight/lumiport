/* order-purge.p - remove cancelled orders */
DEFINE BUFFER bOrd  FOR order.
DEFINE BUFFER bLine FOR order-line.

FOR EACH bOrd WHERE bOrd.status = "cancelled":
    FIND FIRST bLine NO-LOCK WHERE bLine.order-num = bOrd.num NO-ERROR.
    DELETE bOrd.
END.
