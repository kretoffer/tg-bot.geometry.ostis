from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from keyboards.handbook import get_theme_keyboard
from utils.callback_filters import PrefixCallbackFilter

handbook_router = Router()


PAGE_SIZE = 10

async def get_themes_list():
    ... # TODO получение списка тем из БЗ
    return [f"theme {i}" for i in range(1, 51)] # заглушка


@handbook_router.message(F.text == "Справочник")
@handbook_router.message(Command("handbook"))
async def cmd_get_handbook(message: Message):
    themes = await get_themes_list()

    markup = get_theme_keyboard(themes, page=0, page_size=PAGE_SIZE)

    await message.answer("*Справочник:*", parse_mode="markdown", reply_markup=markup)


@handbook_router.callback_query(PrefixCallbackFilter("handbook_page"))
async def handle_page_callback(query: CallbackQuery):
    page = int(query.data.split(":")[1])
    themes = await get_themes_list()
    await query.message.edit_reply_markup(reply_markup=get_theme_keyboard(themes, page=page, page_size=PAGE_SIZE))
