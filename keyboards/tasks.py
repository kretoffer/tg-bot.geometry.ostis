from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_task_markup(task_addr: int):
    keyboard = [
        [InlineKeyboardButton(text="Ответить", callback_data=f"answer2task:{task_addr}")],
        [InlineKeyboardButton(text="Отправить решение", callback_data=f"send-solve2task:{task_addr}")],
        [InlineKeyboardButton(text="Подсказка", callback_data=f"clue2task:{task_addr}")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)