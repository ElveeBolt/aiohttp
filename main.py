import json
import random
import string
import os.path
from aiohttp import web

PATH_JSON = 'links.json'

html_text = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
<form method="POST">
    <input type="text" name="link" placeholder="Введите ссылку">
    <button type="submit">Сократить ссылку</button>
</form>
</body>
</html>
"""


def read_links():
    with open(PATH_JSON, mode='r', encoding='utf-8') as file:
        links = json.load(file)

    return links


def write_links(links: dict):
    with open(PATH_JSON, 'w', encoding='utf-8') as file:
        json.dump(links, file)


async def index(request):
    return web.Response(text=html_text, content_type='text/html')


async def result(request):
    data = await request.post()
    link = data['link']
    links = {}

    new_link = ''.join(random.choice(string.ascii_lowercase) for _ in range(6))

    if os.path.exists(PATH_JSON):
        links = read_links()

    links[new_link] = link
    write_links(links)

    return web.Response(text=f'Ваш код ссылки - {new_link}')


async def redirect(request):
    new_link = request.match_info['new_link']
    links = read_links()
    link = links.get(new_link)

    if link is None:
        raise web.HTTPNotFound(text=f'Ссылка не найдена {new_link}')

    raise web.HTTPFound(link)


app = web.Application()
app.add_routes([
    web.get('/', index),
    web.post('/', result),
    web.get('/{new_link}', redirect)
])

web.run_app(app)
