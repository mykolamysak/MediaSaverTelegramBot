import configparser
import asyncio
import nest_asyncio

from aiogram import Bot, Dispatcher

from src.chat_handler import ChatHandler
from settings.settings import CONFIG_FILE

config = configparser.ConfigParser()
config.read(CONFIG_FILE)
TOKEN = config['Telegram']['TOKEN'].strip()
PROXY_URL = config['Telegram']['PROXY_URL'].strip()

bot = Bot(token=TOKEN, proxy=PROXY_URL)
dp = Dispatcher()

chat_handler = ChatHandler(bot, dp)

async def main():
    print('Bot started.')
    await dp.start_polling(bot)

if __name__ == '__main__':
    nest_asyncio.apply()
    asyncio.run(main())
