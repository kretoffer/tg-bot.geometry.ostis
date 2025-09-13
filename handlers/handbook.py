from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message

from keyboards.themes_keyboard import get_theme_keyboard

from utils.themes import get_themes_list, get_name_of_theme

handbook_router = Router()


PAGE_SIZE = 10


@handbook_router.message(F.text == "Справочник")
@handbook_router.message(Command("handbook"))
async def cmd_get_handbook(message: Message):
    themes = await get_themes_list()
    themes = [get_name_of_theme(theme) for theme in themes]

    markup = get_theme_keyboard("handbook_theme", "themes_page", themes, page=0, page_size=PAGE_SIZE, nav_postfix="handbook_theme")

    await message.answer("*Справочник:*", parse_mode="markdown", reply_markup=markup)
