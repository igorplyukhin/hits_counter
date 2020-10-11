from aiohttp import web
from aiojobs.aiohttp import atomic, setup
import mimetypes
import logging
import time
from datetime import datetime
from cache import cache_request, _cached_requests

time_last_writen_to_db = 11
WRITE_TO_DB_FREQ = 10


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


if __name__ == '__main__':
    app = web.Application()
    app.add_routes([web.get('/', handle),
                    web.get('/{name}', handle)])
    setup(app)
    web.run_app(app, host='192.168.1.215', port=8080)
