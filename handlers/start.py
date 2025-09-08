from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from sc_client.models import ScTemplate, ScLinkContent
from sc_client.client import search_by_template, create_elements

from keyboards.start_keyboards import start_keyboard, start_without_test_keyboard


start_router = Router()

async def check_user_in_sc_machine(user_id: int) -> bool:
    # проверка на наличие пользователя в БЗ TODO
    return False

@start_router.message(CommandStart())
async def cmd_start(message: Message):
    user_id = message.from_user.id
    if await check_user_in_sc_machine(user_id):
        await message.answer("Что вы хотите сделать?",
                             reply_markup=start_keyboard)
    else:
        await message.answer("*Вы пока что не прошли тест*\n" \
        "Вы можете:\n - Пройти тест для разблокировки всех функций \n - Воспользоваться справочником",
        parse_mode="markdown",
        reply_markup=start_without_test_keyboard)
