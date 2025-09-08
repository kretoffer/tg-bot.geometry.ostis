from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from shemes.question import Question


def get_question_keyboard(question: Question):
    keyboard = [
        [InlineKeyboardButton(text=question, callback_data=f"test_answer:{i}")]
        for i, question in enumerate(question.answers)
    ]

    return InlineKeyboardMarkup(inline_keyboard=keyboard)
