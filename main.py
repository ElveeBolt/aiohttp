import json
import random

from aiohttp import web

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


async def index(request):
    return web.Response(text=html_text, content_type='text/html')


async def result(request):
    data = await request.post()
    link = data['link']

    new_link = ''.join(random.choice('0123456789abcd') for _ in range(6))

    with open('links.json', 'a') as file:
        file.write(json.dumps({
            new_link: link
        }))
    return web.Response(text=html_text, content_type='text/html')


async def redirect(request):
    new_link = request.match_info['new_link']
    with open('data.json') as file:
        links = json.load(file)

    link = links.get(new_link)

    if link is None:
        raise web.HTTPNotFound(text=f'Link not Found {new_link}')

    raise web.HTTPFound(link)


app = web.Application()
app.add_routes([
    web.get('/', index),
    web.post('/', result),
    web.get('/{new_link}', redirect)
])

web.run_app(app)
