from aiohttp import web
import hmac
from core import flag_config
from hashlib import md5


def generate_flag(user_id):
    PREFIX = flag_config['prefix']
    SECRET = flag_config['secret'].encode()
    SALT_SIZE = flag_config['salt_size']

    return PREFIX + hmac.new(SECRET, str(user_id).encode(), "sha256").hexdigest()[:SALT_SIZE]


async def handle(request):
    if not request.cookies.get('id'):
        return web.Response(text='Rerun task, I can\'t find your ID', status=400)

    if request.path.replace('/', '') != md5(request.cookies['id'].encode()).hexdigest()[:6]:
        return web.Response(text='Not this one :D')

    flag = generate_flag(request.cookies['id'])
    return web.Response(text=flag)


app = web.Application()
app.add_routes([web.get('/{key:.+}', handle)])

if __name__ == '__main__':
    web.run_app(app)
