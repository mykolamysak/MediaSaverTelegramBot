from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

langMenu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Українська🇺🇦', callback_data='lang_ua')],
    [InlineKeyboardButton(text='English🇬🇧', callback_data='lang_en')]
])