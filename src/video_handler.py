import re
from yt_dlp import YoutubeDL
from aiogram import types

from settings.settings import REGULAR_EXPRESSION
from aiogram.types import URLInputFile

from settings.lang import lang

class VideoHandler:
    def __init__(self):
        self.url_pattern = re.compile(REGULAR_EXPRESSION)

    def is_supported_link(self, url: str) -> bool:
        return self.url_pattern.match(url) is not None

    @staticmethod
    def get_direct_link(video_url: str):
        ydl_options = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'quiet': True,
            'no_warnings': True,
            'outtmpl': '%(id)s.%(ext)s',
        }
        with YoutubeDL(ydl_options) as ydl:
            try:
                info_dict = ydl.extract_info(video_url, download=False)
                formats = info_dict.get('formats', [])
                for fmt in formats:
                    if fmt.get('ext') == 'mp4' and fmt.get('acodec') != 'none' and fmt.get('vcodec') != 'none':
                        return fmt['url'], info_dict.get('title', 'video')
                if 'url' in info_dict:
                    return info_dict['url'], info_dict.get('title', 'video')
            except Exception as e:
                print(f"Error extracting video URL: {e}")
        return None, None

    async def send_video_if_link(self, bot, message: types.Message, trnsl, inline_kb):
        url = message.text.strip()

        if not (url.startswith("http://") or url.startswith("https://")):
            await message.reply(trnsl.translate("That's not a link ", await lang(message)) + '❌')
            return

        if not self.is_supported_link(url):
            await message.reply(trnsl.translate("This link is not supported ", await lang(message)) + '😪')
            return

        direct_link, video_title = self.get_direct_link(url)

        if direct_link:
            try:
                video_file = URLInputFile(direct_link, filename='video@uamediasaver_bot.mp4')
                await bot.send_video(
                    chat_id=message.chat.id,
                    video=video_file,
                    reply_markup=inline_kb
                )
            except Exception as e:
                print(f'Error: {e}')
                await message.reply(trnsl.translate("Sorry, couldn't send the video ", await lang(message)) + '😓')
        else:
            await message.reply(trnsl.translate("Sorry, couldn't fetch the video ", await lang(message)) + '😓')