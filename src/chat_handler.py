import yt_dlp
from aiogram import types, Dispatcher, F
from src.json_handler import JsonHandler
from src.db_handler import Database
from settings import markups as nav
from settings.settings import BOT_URL_START, DB_SECTION

class ChatHandler:
    def __init__(self, bot, dp: Dispatcher):
        self.bot = bot
        self.db = Database(DB_SECTION)
        self.trnsl = JsonHandler()

        self.button_bot_link = types.InlineKeyboardButton(text='🤖 MediaSaver', url=BOT_URL_START)
        self.inline_kb1 = types.InlineKeyboardMarkup(inline_keyboard=[[self.button_bot_link]])

        dp.message.register(self.start_command, F.text == '/start')
        dp.message.register(self.language_command, F.text == '/language')
        dp.message.register(self.handle_message, F.text)
        dp.callback_query.register(self.set_lang_ua_callback, F.data == 'lang_ua')
        dp.callback_query.register(self.set_lang_en_callback, F.data == 'lang_en')

    async def start_command(self, message: types.Message):
        if not self.db.user_exists(message.from_user.id):
            await self.bot.send_message(
                message.from_user.id,
                self.trnsl.translate('Choose language'),
                reply_markup=nav.langMenu
            )
        else:
            await self.send_welcome_message(message)

    async def language_command(self, message: types.Message):
        await self.bot.send_message(
            message.from_user.id,
            self.trnsl.translate('Choose language'),
            reply_markup=nav.langMenu
        )

    async def set_lang_ua_callback(self, callback: types.CallbackQuery):
        await self.bot.delete_message(callback.from_user.id, callback.message.message_id)
        if not self.db.user_exists(callback.from_user.id):
            self.db.add_user(callback.from_user.id, 'UA')
        else:
            self.db.update_lang(callback.from_user.id, 'UA')
        await self.bot.send_message(
            callback.from_user.id,
            self.trnsl.translate('Language set to Ukrainian!', 'UA')
        )

    async def set_lang_en_callback(self, callback: types.CallbackQuery):
        await self.bot.delete_message(callback.from_user.id, callback.message.message_id)
        if not self.db.user_exists(callback.from_user.id):
            self.db.add_user(callback.from_user.id, 'EN')
        else:
            self.db.update_lang(callback.from_user.id, 'EN')
        await self.bot.send_message(
            callback.from_user.id,
            self.trnsl.translate('Language set to English!', 'EN')
        )

    async def handle_message(self, message: types.Message):
        lang = self.db.get_lang(message.from_user.id)
        url = str(message.text).strip()

        if not (url.startswith("http://") or url.startswith("https://")):
            await message.reply(self.trnsl.translate("That's not a link.", lang))
            return

        if not F.text.regexp(r'^https:\/\/('
                             r'www\.youtube.*|youtu\.be.*|youtube\.com.*|'
                             r'www\.instagram\.com.*|instagram\.com.*|'
                             r'www\.tiktok\.com.*|vm\.tiktok\.com.*)').match(url):
            await message.reply(self.trnsl.translate("This link is not supported.", lang))
            return

        direct_link = self.get_direct_link(url)

        if direct_link:
            try:
                await self.bot.send_video(
                    chat_id=message.chat.id,
                    video=direct_link,
                    reply_markup=self.inline_kb1
                )
            except Exception as e:
                await message.answer(self.trnsl.translate("Sorry, couldn't send the video. Error: {}", lang).format(str(e)))
        else:
            await message.answer(self.trnsl.translate("Sorry, couldn't fetch the video.", lang))

    def get_direct_link(self, video_url):
        ydl_options = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'quiet': True,
            'no_warnings': True,
            'outtmpl': '%(id)s.%(ext)s',
        }

        with yt_dlp.YoutubeDL(ydl_options) as ydl:
            info_dict = ydl.extract_info(video_url, download=False)

        formats = info_dict.get('formats', [])
        for fmt in formats:
            if fmt.get('ext') == 'mp4' and fmt.get('acodec') != 'none' and fmt.get('vcodec') != 'none':
                return fmt['url']

        if 'url' in info_dict:
            return info_dict['url']
        return

    async def send_welcome_message(self, message: types.Message):
        await message.answer(
            'Hi!👋\nSend me the link and I will help you to get the video.\n\n'
            'Advantages of MediaSaver:\n'
            '📺 Returns video in .mp4 format;\n'
            '🚫 No ads;\n'
            '🤖 Open source;\n\n'
            '👨‍💻 Contacts: @hglrev',
            reply_markup=self.inline_kb1
        )
