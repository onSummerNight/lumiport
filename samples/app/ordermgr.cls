/* ordermgr.cls - order service */
CLASS ordermgr:

    METHOD PUBLIC INTEGER countOpen():
        DEFINE VARIABLE iCnt AS INTEGER NO-UNDO.
        FOR EACH order NO-LOCK WHERE order.status = "open":
            iCnt = iCnt + 1.
        END.
        RETURN iCnt.
    END METHOD.

    METHOD PUBLIC VOID purge():
        RUN order-purge.p.
    END METHOD.

END CLASS.
