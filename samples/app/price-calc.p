/* price-calc.p - price a line */
DEFINE VARIABLE dPrice AS DECIMAL NO-UNDO.

FIND FIRST item NO-LOCK NO-ERROR.
dPrice = IF AVAILABLE item THEN item.price ELSE 0.

FUNCTION discount RETURNS DECIMAL (INPUT pdAmt AS DECIMAL):
    RETURN pdAmt * 0.9.
END FUNCTION.
