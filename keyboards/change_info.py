from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from config import CHARACTERISTICS, CONTENT_TYPES


change_info_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Класс", callback_data="change-class")],
        [InlineKeyboardButton(text="Характеристики", callback_data="change-charects")],
        [InlineKeyboardButton(text="Предпочтения", callback_data="change-pref")],
    ]
)

change_class_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text=str(i), callback_data=f"change-class:{i}")]
        for i in range(9, 12)
    ]
)

change_charects_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text=el[1], callback_data=f"add-charects:{i}")]
        for i, el in enumerate(CHARACTERISTICS)
    ]
)

change_pref_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text=CONTENT_TYPES[key], callback_data=f"add-pref:{key}")]
        for key in CONTENT_TYPES
    ]
)
