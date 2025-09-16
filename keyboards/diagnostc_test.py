from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from shemes.question import Question


def get_question_keyboard(question: Question):
    keyboard = [
        [InlineKeyboardButton(text=question_text, callback_data=f"test_answer:{question.value}")]
        for question, question_text in question.answers
    ]

    return InlineKeyboardMarkup(inline_keyboard=keyboard)


reg_classes_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text=str(i), callback_data=f"user-reg-class:{i}")]
        for i in range(9, 12)
    ]
)

def get_reg_knowledge_level_keyboard(user_class: int | str):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Низкий", callback_data=f"user-reg-kn-level:{user_class}:bad")],
            [InlineKeyboardButton(text="Нормальный", callback_data=f"user-reg-kn-level:{user_class}:normal")],
            [InlineKeyboardButton(text="Высокий", callback_data=f"user-reg-kn-level:{user_class}:good")],
            [InlineKeyboardButton(text="Олимпиадный", callback_data=f"user-reg-kn-level:{user_class}:olimpyc")]
        ]
    )
