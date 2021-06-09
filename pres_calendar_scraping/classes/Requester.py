from random import randint
from time import time, sleep

import requests

class Requester:

    def __init__(self, min_sleep_time: int, max_sleep_time: int):
        self.min_sleep_time = min_sleep_time
        self.max_sleep_time = max_sleep_time
        self.last_request_at = float('-inf')

    def request(self, method: str, *args, **kwargs) -> requests.Response:
        function = getattr(requests, method)
        wait_since_last_request = randint(self.min_sleep_time, self.max_sleep_time)
        to_wait = self.last_request_at + wait_since_last_request - time()
        if to_wait > 0:
            print(f'Sleeping for {round(to_wait, 2)} s until next request')
            sleep(to_wait)
        print(f'{method.upper()} {args} {kwargs}')
        r = function(*args, **kwargs)
        self.last_request_at = time()
        r.raise_for_status()
        return r