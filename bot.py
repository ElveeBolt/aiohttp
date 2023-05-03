import random
import string
import logging
from aiogram import Bot, Dispatcher, executor, types
from db_utils import get_user_links, insert_link

API_TOKEN = ''

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Привет!\nЯ сокращаю ссылки")


@dp.message_handler(commands=['my_links'])
async def send_welcome(message: types.Message):
    links = await get_user_links(message.from_user.id)
    formated_links = []
    for link in links:
        formated_links.append(f"{link['link']} -> {link['new_link']}\n")
    await message.reply(''.join(formated_links))


@dp.message_handler()
async def send_link(message: types.Message):
    link = message.text
    if link.startswith('http') or link.startswith('https'):
        new_link = ''.join(random.choice(string.ascii_lowercase) for _ in range(6))
        await insert_link(link=link, new_link=new_link, user_id=message.from_user.id)

        await message.answer(new_link)
    else:
        await message.answer('Неверная ссылка')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)