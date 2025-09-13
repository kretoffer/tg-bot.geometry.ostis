from aiogram import Router
from aiogram.types import CallbackQuery

from keyboards.themes_keyboard import get_theme_keyboard

from utils.callback_filters import PrefixCallbackFilter
from utils.themes import get_themes_list, get_name_of_theme

themes_page_router = Router()


PAGE_SIZE = 10


@themes_page_router.callback_query(PrefixCallbackFilter("themes_page"))
async def handle_page_callback(query: CallbackQuery):
    page = int(query.data.split(":")[1])
    prefix = query.data.split(":")[2]
    themes = await get_themes_list()
    themes = [get_name_of_theme(theme) for theme in themes]
    await query.message.edit_reply_markup(reply_markup=get_theme_keyboard(prefix, "themes_page", themes, page=page, page_size=PAGE_SIZE, nav_postfix=prefix))
