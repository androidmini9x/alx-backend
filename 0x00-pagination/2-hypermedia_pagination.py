#!/usr/bin/env python3
'''2. Hypermedia pagination
'''


import csv
import math
from typing import List, Tuple, Dict


def index_range(page: int, page_size: int) -> Tuple[int, int]:
    '''
    return a tuple of size two containing a start index
    and an end index corresponding to the range
    '''
    start = (page - 1) * page_size
    end = start + page_size
    return start, end


class Server:
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        '''Implement get page pages'''
        assert type(page) is int and type(page_size) is int
        assert page > 0 and page_size > 0
        start, end = index_range(page, page_size)
        data = self.dataset()
        if start > len(data):
            return []
        return data[start:end]

    def get_hyper(self, page: int = 1, page_size: int = 10) -> Dict:
        '''Return data as Dictionary (Key->Value)'''
        data = self.get_page(page, page_size)
        start, end = index_range(page, page_size)
        data_length = len(self.__dataset)

        resp = {
            'page_size': len(data),
            'page': page,
            'data': data,
            'next_page': page + 1 if end < data_length else None,
            'prev_page': page - 1 if start > 0 else None,
            'total_pages': math.ceil(data_length / page_size)
        }
        return resp
