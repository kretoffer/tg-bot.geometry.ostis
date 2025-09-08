from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_theme_keyboard(themes: list, page: int = 0, page_size: int = 10):
    start = page * page_size
    end = start + page_size
    page_themes = themes[start:end]

    keyboard = [
        [InlineKeyboardButton(text=theme, callback_data=f"handbook_theme:{themes.index(theme)}")]
        for theme in page_themes
    ]

    nav_buttons = []
    if page > 0:
        nav_buttons.append(InlineKeyboardButton(text="<<", callback_data=f"handbook_page:{page-1}"))
    if end < len(themes):
        nav_buttons.append(InlineKeyboardButton(text=">>", callback_data=f"handbook_page:{page+1}"))

    if nav_buttons:
        keyboard.append(nav_buttons)

    return InlineKeyboardMarkup(inline_keyboard=keyboard)
