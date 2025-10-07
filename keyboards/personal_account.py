from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


personal_account_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Оценить свои знания", callback_data="start_reflection")],
        [InlineKeyboardButton(text="Рефлексия", callback_data="reflection")],
        [InlineKeyboardButton(text="Изменить сложность", callback_data="change-dif")],
        [InlineKeyboardButton(text="Достижения", callback_data="achievements")]
    ]
)

change_gif_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Повысить", callback_data="set-up-kn-level")],
        [InlineKeyboardButton(text="Понизить", callback_data="set-down-kn-level")]
    ]
)

set_up_kn_level_keyboarf = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Пройти тест", callback_data="diagnostic-test")]
        [InlineKeyboardButton(text="Повысить уровень", callback_data="set-up-kn-level-force")]
    ]
)
