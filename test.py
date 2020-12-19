from aiogram import Bot, Dispatcher, executor, filters, types
import asyncio
import logging
from bs4 import BeautifulSoup as bs4
import requests
import os
from aiogram import Bot, Dispatcher, executor, types

API_TOKEN = '1311723678:AAElZga5sq6-7NuUlWV3KAcvT6Hys_hDPYg'

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
url = 'https://inshorts.com/en/read'


class color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


def scrapping():
    page = requests.get(url)
    soup = bs4(page.text, 'html.parser')
    # print(soup.prettify())
    html = soup.prettify()
    div = soup.findAll('div', class_="news-card z-depth-1")
    return div


def image_scraping():
    div = scrapping()
    for thumbs in div:
        tgs = thumbs.find('div', class_="news-card-image")
        tgs1 = tgs['style'].replace("background-image: url('", "")
        thumbnail = tgs1.replace("')", "")
        return thumbnail


def title_scraping():
    div = scrapping()
    for ttl in div:
        title = ttl.find('span', itemprop="headline").getText()
        return title


def body_scraping():
    div = scrapping()
    for bdy in div:
        body = bdy.find('div', itemprop="articleBody").getText()
        return body


@dp.message_handler(filters.CommandStart())
async def send_welcome(message: types.Message):
    # So... At first I want to send something like this:
    await message.reply("Cooking...")

    # Wait a little...
    await asyncio.sleep(1)

    # Good bots should send chat actions...
    await types.ChatActions.upload_photo()

    # Create media group
    media = types.MediaGroup()

    thumbnail = image_scraping()
    title = title_scraping()
    body = body_scraping()
    media.attach_photo(thumbnail,
                       f"<b>{title}</b>\n\n{body}")

    # Done! Send media group
    await message.reply_media_group(media=media)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    # await message.reply("Hi!\nI'm EchoBot!\nPowered by aiogram.")


@dp.message_handler()
async def echo(message: types.Message):
    # old style:
    # await bot.send_message(message.chat.id, message.text)
    await message.reply(message.text)
    print(message.text)
    # await message.answer(message.text)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=False)
