def safeInt(x, base=10):
    '''
    Make an integer from object `x`; return `None` on failure.
    '''

    try:
        result = int(x, base)
    except (ValueError, TypeError):
        result = None
    return result
