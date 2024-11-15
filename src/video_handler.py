import re
from yt_dlp import YoutubeDL
from aiogram import types
from settings.settings import REGULAR_EXPRESSION
from aiogram.types import URLInputFile
from settings.lang import lang
from src.json_handler import JsonHandler


class VideoHandler:
    def __init__(self):
        self.url_pattern = re.compile(REGULAR_EXPRESSION)
        self.trnsl = JsonHandler()

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
                        filesize = fmt.get('filesize') or fmt.get('filesize_approx') or None

                        if filesize:
                            size_mb = round(filesize / (1024 * 1024), 2)
                        else:
                            filesize = info_dict.get('filesize') or info_dict.get('filesize_approx') or None
                            size_mb = round(filesize / (1024 * 1024), 2) if filesize else None

                        return {
                            'url': fmt['url'],
                            'title': info_dict.get('title', 'video'),
                            'author': info_dict.get('uploader', 'Unknown'),
                            'description': info_dict.get('description', 'No description')[:40],
                            'duration': info_dict.get('duration', 0),
                            'original_url': video_url,
                            'size': size_mb,
                        }

                if 'url' in info_dict:
                    filesize = info_dict.get('filesize') or info_dict.get('filesize_approx') or None
                    size_mb = round(filesize / (1024 * 1024), 2) if filesize else None

                    return {
                        'url': info_dict['url'],
                        'title': info_dict.get('title', 'video'),
                        'author': info_dict.get('uploader', 'Unknown'),
                        'description': info_dict.get('description', 'No description')[:40],
                        'duration': info_dict.get('duration', 0),
                        'original_url': video_url,
                        'size': size_mb,
                    }
            except Exception as e:
                print(f"Error extracting video URL: {e}")
        return None

    async def send_video_if_link(self, bot, message: types.Message, trnsl, inline_kb):
        if message.chat.type != 'private':
            url = message.text.strip()
            if not (url.startswith("http://") or url.startswith("https://")):
                return

            if not self.is_supported_link(url):
                return

        url = message.text.strip()

        if not (url.startswith("http://") or url.startswith("https://")):
            await message.reply(trnsl.translate("That's not a link ", await lang(message)) + '❌')
            return

        if not self.is_supported_link(url):
            await message.reply(trnsl.translate("This link is not supported ", await lang(message)) + '😪')
            return

        video_info = self.get_direct_link(url)

        if video_info and video_info['url']:
            try:
                if video_info['size'] and video_info['size'] > 50:
                    await message.reply(trnsl.translate("The bot cannot process videos that are more than 50 MB ",
                                                        await lang(message)) + '🤐')
                duration_minutes, duration_seconds = divmod(int(video_info['duration']), 60)

                size_text = f"{video_info['size']:.2f} MB" if video_info['size'] is not None else ""

                caption_parts = [
                    f'👤 {video_info["author"]}',
                    f'📃 {video_info["description"]}...',
                    f'⌛ {duration_minutes}:{duration_seconds:02d}',
                    f'🔗 <a href="{video_info["original_url"]}">{self.trnsl.translate("Link to original video", await lang(message))}</a>'
                ]

                if size_text:
                    caption_parts.append(f"🧿 {size_text}")

                caption_parts.append("\n@uamediasaver_bot")

                video_caption = "\n".join(caption_parts)

                video_file = URLInputFile(video_info['url'], filename='video@uamediasaver_bot.mp4')
                await bot.send_video(
                    chat_id=message.chat.id,
                    video=video_file,
                    caption=video_caption,
                    reply_markup=inline_kb,
                    parse_mode='HTML'
                )
            except Exception as e:
                print(f'Error: {e}')
                await message.reply(trnsl.translate("Sorry, couldn't send the video ", await lang(message)) + '😓')
        else:
            await message.reply(trnsl.translate("Sorry, couldn't fetch the video ", await lang(message)) + '😓')

