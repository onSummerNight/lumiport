/* report.p - order report
   /* nested note: RUN ghost.p must be ignored */
   FOR EACH phantom NO-LOCK: still inside the outer comment
*/
{common.i}

MESSAGE "RUN fake.p and FOR EACH decoy" VIEW-AS ALERT-BOX.
MESSAGE 'CREATE ghost-row' VIEW-AS ALERT-BOX.

FOR EACH order NO-LOCK:
    FIND customer NO-LOCK WHERE customer.code = order.cust-code NO-ERROR.
    RUN printLine (INPUT order.num).
END.

PROCEDURE printLine:
    DEFINE INPUT PARAMETER piNum AS INTEGER NO-UNDO.
    MESSAGE STRING(piNum).
END PROCEDURE.
