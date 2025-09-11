from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


select_knowledge_level_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Низкий", callback_data="self-kn-level:bad")],
        [InlineKeyboardButton(text="Нормальный", callback_data="self-kn-level:normal")],
        [InlineKeyboardButton(text="Высокий", callback_data="self-kn-level:good")],
        [InlineKeyboardButton(text="Олимпиадный", callback_data="self-kn-level:olimpyc")]
    ]
)
