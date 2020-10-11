from datetime import datetime
import os

_cached_requests = []


def cache_request(ip, req_path):
    time_zone = datetime.now().astimezone().tzinfo
    date = datetime.now().strftime(f'[%d/%m/%Y:%H:%M:%S {time_zone}]')
    _cached_requests.append(f'{ip} {date} {req_path}')
