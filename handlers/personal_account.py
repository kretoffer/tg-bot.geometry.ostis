from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message

from utils.get_user import get_user_info

from keyboards.personal_account import personal_account_keyboard
from keyboards.start_keyboards import start_without_test_keyboard

from config import START_PHRASE_WITHOUT_TEST

personal_accaunt_router = Router()


@personal_accaunt_router.message(F.text.lower() == "личный кабинет")
@personal_accaunt_router.message(Command("accaunt"))
async def cmd_accaunt(message: Message):
    user_info = get_user_info(message.chat.id)
    if not user_info:
        await message.answer(text=START_PHRASE_WITHOUT_TEST, parse_mode="markdown", reply_markup=start_without_test_keyboard)
        return
    await message.answer(str(user_info), parse_mode="markdown", reply_markup=personal_account_keyboard)
