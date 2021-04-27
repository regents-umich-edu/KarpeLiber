from functools import reduce
from operator import and_
from typing import Optional, Any

from django.db.models import Q


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


def queryAllWords(columnAndOperator: str, searchString: str) -> Q:
    '''
    Split `searchString` into whitespace-delimited words and combine them
    together with the `columnAndOperator` using the `and_` operator.

    :param columnAndOperator: A Django column name and operator,
        like `name__icontains`.
    :param searchString: A string to search for.
    :return: A Django query object, Q.
    '''

    # TODO: add `not` support for words beginning with `-` (a la Google)
    return reduce(and_, (Q((columnAndOperator, word)) for word in
                         searchString.split()))
