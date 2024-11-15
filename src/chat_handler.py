from aiogram import types, Dispatcher, F

from src.db_handler import Database
from src.json_handler import JsonHandler
from src.video_handler import VideoHandler
from settings.settings import DB_SECTION, BOT_URL_START, BOT_URL_ADD_TO_GROUP_CHAT
from settings import markups as nav
from settings.lang import lang

class ChatHandler:
    def __init__(self, bot, dp: Dispatcher):
        self.bot = bot
        self.db = Database(DB_SECTION)
        self.trnsl = JsonHandler()
        self.video_handler = VideoHandler()

        self.button_bot_link = types.InlineKeyboardButton(text='🤖 MediaSaver', url=BOT_URL_START)
        self.button_add_bot_to_group_chat = types.InlineKeyboardButton(text='👥 Add to chat', url=BOT_URL_ADD_TO_GROUP_CHAT)
        self.inline_welcome = types.InlineKeyboardMarkup(inline_keyboard=[[self.button_bot_link]])
        self.inline_add_to_group_chat = types.InlineKeyboardMarkup(inline_keyboard=[[self.button_add_bot_to_group_chat]])

        dp.message.register(self.start_command, F.text == '/start')
        dp.message.register(self.info_command, F.text == '/info')
        dp.message.register(self.language_command, F.text == '/language')
        dp.message.register(self.add_to_group_chat_command, F.text == '/add')
        dp.message.register(self.handle_message, F.text)

        dp.callback_query.register(self.set_lang_ua_callback, F.data == 'lang_ua')
        dp.callback_query.register(self.set_lang_en_callback, F.data == 'lang_en')

    async def start_command(self, message: types.Message):
        if not self.db.user_exists(message.from_user.id):
            self.db.add_user(message.from_user.id, 'EN')
        await message.answer(self.trnsl.translate('Send me the link and I will send you the video in the chat ', await lang(message)) + '🔗👇')


    async def info_command(self, message: types.Message):
        await self.bot.send_message(
            message.from_user.id,
            self.trnsl.translate('🤖 MediaSaver is a bot for downloading videos from YouTube, Instagram, and TikTok.\n\n'
                                 'Just choose your preferred language (🇺🇦/🇬🇧) and send a link to the video you want to save.\n'
                                 'I support links from youtube.com, youtu.be, instagram.com, tiktok.com, and vm.tiktok.com.\n\n'
                                 'For a successful upload, make sure the video is public, send only one link at a time, '
                                 'and wait a few seconds for processing.\n\n'
                                 'Share the bot with your friends:\n@uamediasaver_bot',
                                 await lang(message)), reply_markup=self.inline_welcome
        )

    async def language_command(self, message: types.Message):
        await self.bot.send_message(
            message.from_user.id,
            self.trnsl.translate('Choose the language ', await lang(message)) +'🌍',
            reply_markup=nav.langMenu
        )

    async def add_to_group_chat_command(self, message: types.Message):
        await self.bot.send_message(
            message.from_user.id,
            self.trnsl.translate(
                'To add the bot to your group chat press button below and select the chat from the list ', await lang(message)) + '⬇',
            reply_markup=self.inline_add_to_group_chat
        )

    async def set_lang_ua_callback(self, callback: types.CallbackQuery):
        await self.bot.delete_message(callback.from_user.id, callback.message.message_id)
        if not self.db.user_exists(callback.from_user.id):
            self.db.add_user(callback.from_user.id, 'UA')
        else:
            self.db.update_lang(callback.from_user.id, 'UA')
        await self.bot.send_message(
            callback.from_user.id,
            self.trnsl.translate('Вибрано українську мову! ', 'UA') + '🇺🇦'
        )

    async def set_lang_en_callback(self, callback: types.CallbackQuery):
        await self.bot.delete_message(callback.from_user.id, callback.message.message_id)
        if not self.db.user_exists(callback.from_user.id):
            self.db.add_user(callback.from_user.id, 'EN')
        else:
            self.db.update_lang(callback.from_user.id, 'EN')
        await self.bot.send_message(
            callback.from_user.id,
            self.trnsl.translate('Language set to English! ', 'EN') + '🇬🇧'
        )

    async def handle_message(self, message: types.Message):
        await self.video_handler.send_video_if_link(self.bot, message, self.trnsl, self.inline_welcome)