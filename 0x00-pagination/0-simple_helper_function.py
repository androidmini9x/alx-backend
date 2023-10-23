#!/usr/bin/env python3
'''0. Simple helper function
'''


from typing import Tuple


def index_range(page: int, page_size: int) -> Tuple[int, int]:
    '''
    return a tuple of size two containing a start index
    and an end index corresponding to the range
    '''
    start = (page - 1) * page_size
    end = start + page_size
    return start, end
