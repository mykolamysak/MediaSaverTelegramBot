# MediaSaver Telegram Bot 💾

## Description 📄
**MediaSaver Telegram Bot** is a bot for downloading and saving media from Instagram Reels, TikTok Videos and Youtube.
## Features🌵
- Language selection(UA/EN)
- Detailed video description: author, video desc, duration, link, size
- Special filename
- Smart UsersDB
- Translations

## Installation 🔨
### 1. Clone the Repository
```sh
git clone https://github.com/mykolamysak/MediaSaverTelegramBot.git
cd MediaSaver
```

### 2. Install Dependencies
Ensure you have Python 3.8+
```sh
pip install -r requirements.txt
```

### 3. Configuration
Create a `.env` file in the root directory and specify your bot token:
```ini
BOT_TOKEN=your_telegram_bot_token
SAVE_PATH=./media/
```

### 4. Run
```shell
python main.py
```

## Usage 🎥
- Send a link to the bot and get the video

![]([https://imgur.com/a/r0JkEcZ](https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExOXdrb2Qyajc0MmV0cjlnNmhpb2Jzc241bmF6dm9tY3hlMm5sMjVpeiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/V1puxnUuSebcvlNUqL/giphy.gif))

## Libraries Used 📁
- `aiogram` (~=3.14.0) - A modern and efficient framework for building Telegram bots using Python and asynchronous programming.
- `requests` (~=2.32.3) - A simple yet powerful library for making HTTP requests, used for interacting with APIs.
- `yt-dlp` (~=2024.11.4) - A powerful tool for downloading media from YouTube and other streaming platforms.
- `nest-asyncio` (~=1.6.0) - A library that allows nested use of `asyncio` event loops, making it easier to run async functions in environments like Jupyter notebooks or interactive shells.



## Author 👷
Mykola Mysak

## License 🔐
This project is licensed under the [MIT License](LICENSE).





