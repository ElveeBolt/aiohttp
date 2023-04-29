import os.path
import random
import string

import aiohttp_jinja2
import jinja2
from aiohttp import web

from aiopg.sa import create_engine
import sqlalchemy as sa

metadata = sa.MetaData()

tbl = sa.Table(
    'links', metadata,
    sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
    sa.Column('link', sa.String(255)),
    sa.Column('new_link', sa.String(255))
)


async def init_pg():
    engine = await create_engine(
        user='postgres',
        database='postgres',
        host=os.getenv('POSTGRES_HOST', '127.0.0.1'),
        password='postgres',
        port=5432
    )
    return engine


async def insert_link(link, new_link):
    engine = await init_pg()
    async with engine.acquire() as connection:
        await connection.execute(tbl.insert().values(link=link, new_link=new_link))


async def get_link(new_link):
    engine = await init_pg()
    async with engine.acquire() as connection:
        result = await connection.execute(tbl.select().where(tbl.c.new_link == new_link))
        result = await result.first()
    return result


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
