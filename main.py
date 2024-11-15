import configparser
import asyncio
from aiogram import Bot, Dispatcher
import nest_asyncio
from src.chat_handler import ChatHandler
from settings.settings import CONFIG_FILE

config = configparser.ConfigParser()
config.read(CONFIG_FILE)
TOKEN = config['Telegram']['TOKEN'].strip()

bot = Bot(TOKEN)
dp = Dispatcher()

chat_handler = ChatHandler(bot, dp)

async def main():
    print('Bot started.')
    await dp.start_polling(bot)

if __name__ == '__main__':
    nest_asyncio.apply()
    asyncio.run(main())
