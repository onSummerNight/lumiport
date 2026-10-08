/* util.i - string helpers */
FUNCTION trimAll RETURNS CHARACTER (INPUT pcText AS CHARACTER):
    RETURN TRIM(pcText).
END FUNCTION.
