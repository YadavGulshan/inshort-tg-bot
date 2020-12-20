from aiogram import Bot, Dispatcher, executor, types
import asyncio
import logging
from bs4 import BeautifulSoup as bs4
import requests
from time import sleep


API_TOKEN = 'token'
# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


def scrapping():
    url = 'https://inshorts.com/en/read'
    page = requests.get(url)
    soup = bs4(page.text, 'html.parser')
    # print(soup.prettify())
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


def authorIs():
    div = scrapping()
    for auth in div:
        authorAndTime = auth.find(
            'div', class_="news-card-author-time news-card-author-time-in-title").getText()
        return authorAndTime


def readmoreLink():
    div = scrapping()
    for read in div:
        read1 = read.find('div', class_="read-more").getText()
        return read1


def hrefstuff():
    hr = scrapping()
    for readmorelinkis in hr:
        readmore = readmorelinkis.find('a', class_="source").get("href")
        return readmore


@dp.message_handler(commands=['hey'])
async def inshort(message: types.Message):

    thumbnail = image_scraping()
    title = title_scraping()
    body = body_scraping()
    author = authorIs().replace("short", "")
    readmore = readmoreLink()
    href = hrefstuff()

    await bot.send_photo(chat_id=message.chat.id,
                         photo=thumbnail, caption=f"<b>{title}</b>\n\n{body}\n{author}\n<a href='{href}'>{readmore}</a>", parse_mode="HTML")


@dp.message_handler(commands=['get'])
async def send_welcome(message: types.Message):
    await message.reply("Hi!\nI'm EchoBot!\nPowered by aiogram.")
    await inshort(message)


@dp.message_handler(commands=['start'])
async def main(message: types.Message):
    i = 1
    await inshort(message)
    temp = title_scraping()
    while(i == 1):
        if(temp == title_scraping()):
            print("Haven't found something new")
            await asyncio.sleep(30)
        else:
            await inshort(message)
            temp = title_scraping()
            print("I got something")


@dp.message_handler()
async def echo(message: types.Message):
    # old style:
    # await bot.send_message(message.chat.id, message.text)
    await message.reply(message.text)
    # print(message.text)
    # await message.answer(message.text)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=False)


# print(image_scraping())
