/* order-create.p - create an order with lines */
{common.i}
{util.i}

DEFINE INPUT PARAMETER pcCustCode AS CHARACTER NO-UNDO.

FIND customer NO-LOCK WHERE customer.code = pcCustCode NO-ERROR.
IF NOT AVAILABLE customer THEN RETURN.

CREATE order.
order.cust-code = pcCustCode.

RUN addLine.
RUN price-calc.p.

PROCEDURE addLine:
    CREATE order-line.
    order-line.order-num = order.num.
END PROCEDURE.

FUNCTION fmtMoney RETURNS CHARACTER (INPUT pdAmt AS DECIMAL):
    RETURN trimAll(STRING(pdAmt)).
END FUNCTION.
