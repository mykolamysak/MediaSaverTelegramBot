import re
from yt_dlp import YoutubeDL
from aiogram import types
from aiogram.types import URLInputFile
import requests
from settings.settings import REGULAR_EXPRESSION
from settings.lang import lang
from src.json_handler import JsonHandler


class VideoHandler:
    def __init__(self):
        self.url_pattern = re.compile(REGULAR_EXPRESSION)
        self.trnsl = JsonHandler()
        self.tiktok_headers = {
            "x-rapidapi-key": "b0c549c053mshd503eb154fe3a31p1a71ecjsnba92791dbaec",
            "x-rapidapi-host": "tiktok-video-no-watermark2.p.rapidapi.com"
        }
        self.tiktok_api_url = "https://tiktok-video-no-watermark2.p.rapidapi.com"

    def is_supported_link(self, url: str) -> bool:
        return self.url_pattern.match(url) is not None

    @staticmethod
    def get_youtube_link(video_url: str):
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
            except Exception as e:
                print(f"Error extracting video URL: {e}")
        return

    def get_tiktok_link(self, video_url: str):
        querystring = {"url": video_url, "hd": "1"}
        try:
            response = requests.get(self.tiktok_api_url, headers=self.tiktok_headers, params=querystring)
            response_json = response.json()

            video_link = response_json['data'].get('play', None)
            if video_link:
                title = response_json['data'].get('title', 'TikTok Video')
                author_nickname = response_json['data'].get('author', {}).get('nickname', 'TikTok User')
                author_avatar = response_json['data'].get('author', {}).get('avatar', '')
                description = response_json['data'].get('description', 'No description available')
                duration = response_json['data'].get('duration', 0)

                return {
                    'url': video_link,
                    'title': title,
                    'author': author_nickname,
                    'avatar': author_avatar,
                    'description': description[:100],
                    'duration': duration,
                    'original_url': video_url,
                    'size': None,
                }
        except Exception as e:
            print(f"Error fetching TikTok video link: {e}")
        return

    async def send_video_if_link(self, bot, message: types.Message, trnsl, inline_kb):
        if message.chat.type not in ['group', 'supergroup']:
            return

        url = message.text.strip()
        if not (url.startswith("http://") or url.startswith("https://")) or not self.is_supported_link(url):
            return

        if "tiktok.com" in url:
            video_info = self.get_tiktok_link(url)
        else:
            video_info = self.get_youtube_link(url)

        if not video_info or not video_info.get('url'):
            await message.reply(trnsl.translate("Sorry, couldn't fetch the video ", await lang(message)) + '😓')
            return

        try:
            if video_info['size'] and video_info['size'] > 50:
                await message.reply(trnsl.translate("The bot cannot process videos that are more than 50 MB ",
                                                    await lang(message)) + '🤐')
                return

            duration_minutes, duration_seconds = divmod(int(video_info['duration']), 60)

            caption_parts = [f'👤 {video_info["author"]}']

            if video_info.get('duration'):
                caption_parts.append(f'⌛ {duration_minutes}:{duration_seconds:02d}')

            if video_info.get('size'):
                caption_parts.append(f"🧿 {video_info['size']:.2f} MB")

            caption_parts.append(
                f'🔗 <a href="{video_info["original_url"]}">{self.trnsl.translate("Link to original video", await lang(message))}</a>')
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
