import os.path
import random
import string

import aiohttp_jinja2
import jinja2
from aiohttp import web
from db_utils import insert_link, get_link



@aiohttp_jinja2.template('index.html')
async def index(request):
    return {}


@aiohttp_jinja2.template('result.html')
async def result(request):
    data = await request.post()
    link = data['link']

    new_link = ''.join(random.choice(string.ascii_lowercase) for _ in range(6))

    await insert_link(link=link, new_link=new_link)

    return {'new_link': new_link}


async def redirect(request):
    new_link = request.match_info['new_link']

    link = await get_link(new_link)

    if link is None:
        raise web.HTTPNotFound(text=f'Ссылка не найдена {new_link}')

    raise web.HTTPFound(link['link'])


if __name__ == '__main__':
    app = web.Application()

    aiohttp_jinja2.setup(
        app, loader=jinja2.FileSystemLoader(os.path.join(os.getcwd(), 'templates'))
    )

    app.add_routes([
        web.get('/', index),
        web.post('/', result),
        web.get('/{new_link}', redirect)
    ])

    web.run_app(app)
