from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from shemes.question import Question


def get_question_keyboard(question: Question):
    keyboard = [
        [InlineKeyboardButton(text=question_text, callback_data=f"test_answer:{question.value}")]
        for question, question_text in question.answers
    ]

    return InlineKeyboardMarkup(inline_keyboard=keyboard)
