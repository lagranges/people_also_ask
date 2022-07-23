#! /usr/bin/env python3
import time
import random
import traceback
from contextlib import ContextDecorator
from typing import Callable, List
from people_also_ask.exceptions import FeaturedSnippetParserError


def raise_featuredsnippetparsererror_if_failed(func):
    def wrapper(self: "SimpleFeaturedSnippetParser", *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except Exception:
            traceback.print_exc()
            raise FeaturedSnippetParserError(self.text)
    return wrapper


def retryable(nb_times_retry):

    def decorator(func: Callable):

        def wrapper(*args, **kwargs):
            for _ in range(nb_times_retry-1):
                try:
                    return func(*args, **kwargs)
                except Exception:
                    pass
            return func(*args, **kwargs)

        return wrapper
    return decorator


def itemize(lines: List[str]) -> List[str]:
    return ["\t- " + line for line in lines]


def tabulate(header, table):
    length_columns = []
    if header:
        table = [header] + table
        length_columns = [len(str(e)) for e in header]
    for row in table:
        current_lengh = [len(str(e)) for e in row]
        length_columns = [
            max(i, j) for i, j in zip(length_columns, current_lengh)
        ]
    tabulated_rows = []
    for row in table:
        tabulated_rows.append("\t".join([
            str(e).rjust(length, " ") for e, length in zip(row, length_columns)
        ]))
    if header:
        tabulated_rows.insert(
            1,
            "\t".join(["-"*length for length in length_columns])
        )
    return "\n".join(tabulated_rows)


def remove_redundant(elements): return list(dict.fromkeys(elements))


class CallingSemaphore(ContextDecorator):

    def __init__(self, nb_call_times_limit, expired_time):
        self.nb_call_times_limit = nb_call_times_limit
        self.expired_time = expired_time
        self.called_timestamps = list()

    def __enter__(self):
        while len(self.called_timestamps) > self.nb_call_times_limit:
            now = time.time()
            self.called_timestamps = list(filter(
                lambda x: now - x < self.expired_time,
                self.called_timestamps
            ))
            time.sleep(random.random() * 2)
        self.called_timestamps.append(time.time())

    def __exit__(self, *exc):
        pass
