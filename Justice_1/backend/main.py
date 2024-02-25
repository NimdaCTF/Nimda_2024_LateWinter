from aiohttp import web
from core import config
import hashlib
import asyncio
import time


async def get_hash(val):
    sha512 = hashlib.sha512()
    sha512.update(val.encode('utf-8'))
    return sha512.hexdigest()


async def check_hash(input_string):
    dt_pool = [int(time.time()) - i for i in range(3)]
    hash_tasks = [get_hash(str(x)) for x in dt_pool]

    hash_results = await asyncio.gather(*hash_tasks)

    return input_string in hash_results


async def handle(request):
    try:
        data = await request.json()
        login = data.get('login', '')
        password = data.get('password', '')
        key = data.get('key', '')

        if login != config['login'] or password != config['password'] or not await check_hash(key):
            return web.Response(text='No :^)', status=401)

        return web.Response(text='Ok', status=200)
    except Exception as e:
        return web.Response(text='No :^)', status=401)


app = web.Application()
app.add_routes([web.post('/login', handle)])

if __name__ == '__main__':
    web.run_app(app)
