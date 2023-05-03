import os
from aiopg.sa import create_engine
import sqlalchemy as sa

metadata = sa.MetaData()

tbl = sa.Table(
    'links', metadata,
    sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
    sa.Column('link', sa.String(255)),
    sa.Column('new_link', sa.String(255)),
    sa.Column('user_id', sa.Integer()),
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


async def insert_link(link, new_link, user_id=None):
    engine = await init_pg()
    async with engine.acquire() as connection:
        await connection.execute(tbl.insert().values(link=link, new_link=new_link, user_id=user_id))


async def get_link(new_link):
    engine = await init_pg()
    async with engine.acquire() as connection:
        result = await connection.execute(tbl.select().where(tbl.c.new_link == new_link))
        result = await result.first()
    return result


async def get_user_links(user_id):
    engine = await init_pg()
    async with engine.acquire() as connection:
        results = await connection.execute(tbl.select().where(tbl.c.user_id == user_id))
        results = await results.fetchall()
    return [{'link': result['link'], 'new_link': result['new_link']} for result in results]