from typing import Optional, Any


def safeInt(x: Any, base: int = 10) -> Optional[int]:
    '''
    Make an integer from object `x`; return `None` on failure.
    '''

    result: Optional[int]

    try:
        result = int(x, base)
    except (ValueError, TypeError):
        result = None

    return result
