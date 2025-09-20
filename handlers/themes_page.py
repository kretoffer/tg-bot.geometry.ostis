from aiogram import Router
from aiogram.types import CallbackQuery

from keyboards.themes_keyboard import get_theme_keyboard

from utils.callback_filters import PrefixCallbackFilter
from utils.themes import get_themes_list
from utils.get_idtf import get_name_str

themes_page_router = Router()


PAGE_SIZE = 10


@themes_page_router.callback_query(PrefixCallbackFilter("themes_page"))
async def handle_page_callback(query: CallbackQuery):
    page = int(query.data.split(":")[1])
    prefix = query.data.split(":")[2]
    themes = await get_themes_list()
    indexes = [theme.value for theme in themes]
    themes = [get_name_str(theme) for theme in themes]
    await query.message.edit_reply_markup(reply_markup=get_theme_keyboard(prefix, "themes_page", themes, indexes, page=page, page_size=PAGE_SIZE, nav_postfix=prefix))
