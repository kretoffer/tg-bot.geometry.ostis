from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


start_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Уроки")],
        [KeyboardButton(text="Задачи")],
        [KeyboardButton(text="Тесты")],
        [KeyboardButton(text="Справочник")],
        [KeyboardButton(text="Личный кабинет")]
    ],
    resize_keyboard=True
)

start_without_test_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Пройти тест")],
        [KeyboardButton(text="Справочник")]
    ],
    resize_keyboard=True
)