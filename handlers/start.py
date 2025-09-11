from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from keyboards.start_keyboards import start_keyboard, start_without_test_keyboard

from utils.get_user import check_user_in_sc_machine

from config import START_PHRASE, START_PHRASE_WITHOUT_TEST


start_router = Router()

@start_router.message(CommandStart())
async def cmd_start(message: Message):
    user_id = message.from_user.id
    if await check_user_in_sc_machine(user_id):
        await message.answer(START_PHRASE,
                             reply_markup=start_keyboard)
    else:
        await message.answer(START_PHRASE_WITHOUT_TEST,
        parse_mode="markdown",
        reply_markup=start_without_test_keyboard)
