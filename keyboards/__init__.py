from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

free_inline_markup = InlineKeyboardMarkup(
    inline_keyboard=[]
)

def get_stop_keyboard(prefix: str, postfix: str = "") -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Закончить", callback_data=f"{prefix}-stop:{postfix}")]
        ]
    )
