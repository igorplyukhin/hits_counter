from aiohttp import web
from aiojobs.aiohttp import atomic, setup
import mimetypes
import logging
import time
from datetime import datetime
from cache import cache_request, _cached_requests
import multiprocessing
import subprocess
import requests

time_last_writen_to_db = 11
WRITE_TO_DB_FREQ = 10
HOST = '127.0.0.1'
PORT = 8080


@atomic
async def handle(request):
    global time_last_writen_to_db
    try:
        f = open(f'static{request.path}', 'rb')
    except (FileNotFoundError, IsADirectoryError):
        return web.HTTPFound('/hamming.html')
    body = f.read()
    f.close()
    cache_request(request.remote, request.path)
    if time.time() - time_last_writen_to_db > WRITE_TO_DB_FREQ:
        time_last_writen_to_db = time.time()
        pass
    return web.Response(body=body, content_type=mimetypes.guess_type(request.path)[0])


async def proxy_to_bd_server(request):
    r = requests.get(url=f'http://127.0.0.1:5000{request.path_qs}')
    content_type = r.headers['Content-Type'].split(';')[0]  # trim charset utf-8
    return web.Response(body=r.text, content_type=content_type)


def run_statistic_server():
    subprocess.Popen(['sqlite_web', '-p', '5000', '-u', '/stats', '--no-browser', '--read-only',
                      'hits_counter.sqlite'])


def run_custom_server():
    app = web.Application()
    app.add_routes([web.get('/', handle),
                    web.get(r'/{statistic:stats.*}', proxy_to_bd_server),
                    web.get('/{name}', handle)])
    setup(app)
    web.run_app(app, host=HOST, port=PORT)


if __name__ == '__main__':
    p = multiprocessing.Process(target=run_statistic_server())
    p.start()
    run_custom_server()
