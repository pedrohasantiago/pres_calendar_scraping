from time import time, sleep

import requests

class Requester:

    def __init__(self, seconds_between_requests: int):
        self.seconds_between_requests = seconds_between_requests
        self.last_request_at = float('-inf')

    def request(self, method: str, *args, **kwargs) -> requests.Response:
        function = getattr(requests, method)
        to_wait = self.last_request_at + self.seconds_between_requests - time()
        if to_wait > 0:
            print(f'Sleeping for {to_wait} s until next request')
            sleep(to_wait)
        print(f'{method.upper()} {args} {kwargs}')
        r = function(*args, **kwargs)
        self.last_request_at = time()
        r.raise_for_status()
        return r