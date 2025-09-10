from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from shemes.question import Question


personal_account_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Оценить свои знания", callback_data="start_reflection")],
        [InlineKeyboardButton(text="Достижения", callback_data="achievements")]
    ]
)
