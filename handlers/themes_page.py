from aiogram import Router
from aiogram.types import CallbackQuery

from keyboards.themes_keyboard import get_theme_keyboard

from utils.callback_filters import PrefixCallbackFilter
from utils.themes import get_themes_list
from utils.get_idtf import get_name_str
from utils.recomendations import get_recomendate_themes, get_recommendated_lessons, get_recomendate_tasks, get_recomendate_tests
from utils.get_user import get_user

themes_page_router = Router()


PAGE_SIZE = 10

COMPARATORS = {
    "lesson-theme": get_recomendate_themes,
    "test-theme": get_recomendate_themes,
    "task-theme": get_recomendate_themes,
    "start-lesson": get_recommendated_lessons,
    "test-start": get_recomendate_tests
}

NAME_COMPARATORS = {
    "start-lesson": lambda lesson: lesson.value,
    "test-start": lambda test: test.value,
    
}


@themes_page_router.callback_query(PrefixCallbackFilter("themes_page"))
async def handle_page_callback(query: CallbackQuery):
    page = int(query.data.split(":")[1])
    prefix = query.data.split(":")[2]
    postfix = ":".join(query.data.split(":")[2:])
    if prefix not in COMPARATORS:
        themes = await get_themes_list()
    else:
        user = get_user(query.message.chat.id)
        themes = await COMPARATORS[prefix](user=user, data=query.data)
    indexes = [theme.value for theme in themes]
    if prefix not in NAME_COMPARATORS:
        get_name = get_name_str
    else:
        NAME_COMPARATORS[prefix]
    themes = [get_name(theme) for theme in themes]
    await query.message.edit_reply_markup(reply_markup=get_theme_keyboard(prefix, "themes_page", themes, indexes, page=page, page_size=PAGE_SIZE, nav_postfix=postfix))
