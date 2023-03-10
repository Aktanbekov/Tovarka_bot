from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

kg = KeyboardButton('/KGZ🇰🇬')
ru = KeyboardButton('/RU🇷🇺')

greet_kb = ReplyKeyboardMarkup(
    resize_keyboard=True, one_time_keyboard=True).add(kg).add(ru)
blank_kb = ReplyKeyboardRemove()
