from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_theme_keyboard(prefix: str, nav_prefix: str, themes: list, page: int = 0, page_size: int = 10, nav_postfix: str = ""):
    start = page * page_size
    end = start + page_size
    page_themes = themes[start:end]

    keyboard = [
        [InlineKeyboardButton(text=theme, callback_data=f"{prefix}:{themes.index(theme)}")]
        for theme in page_themes
    ]

    nav_buttons = []
    if page > 0:
        nav_buttons.append(InlineKeyboardButton(text="<<", callback_data=f"{nav_prefix}:{page-1}:{nav_postfix}"))
    if end < len(themes):
        nav_buttons.append(InlineKeyboardButton(text=">>", callback_data=f"{nav_prefix}:{page+1}:{nav_postfix}"))

    if nav_buttons:
        keyboard.append(nav_buttons)

    return InlineKeyboardMarkup(inline_keyboard=keyboard)
