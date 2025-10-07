from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from utils.get_user import get_user_info, get_user

from keyboards.personal_account import personal_account_keyboard, change_gif_keyboard
from keyboards.start_keyboards import start_without_test_keyboard

from config import START_PHRASE_WITHOUT_TEST

from utils.create_action import create_action

personal_accaunt_router = Router()


@personal_accaunt_router.message(F.text.lower() == "личный кабинет")
@personal_accaunt_router.message(Command("accaunt"))
async def cmd_accaunt(message: Message):
    user_info = get_user_info(message.chat.id)
    if not user_info:
        await message.answer(text=START_PHRASE_WITHOUT_TEST, parse_mode="markdown", reply_markup=start_without_test_keyboard)
        return
    await message.answer(str(user_info), parse_mode="markdown", reply_markup=personal_account_keyboard)


@personal_accaunt_router.callback_query(F.data == "change-dif")
async def change_kn_level(query: CallbackQuery):
    await query.message.edit_text(
        text="Вы хотите повысить или понизить сложность?",
        reply_markup=change_gif_keyboard
    )


@personal_accaunt_router.callback_query(F.data == "set-up-kn-level")
async def change_kn_level_up_q(query: CallbackQuery):
    await query.message.edit_text(
        text="Вы желаете пройти тест для определения уровня знаний или повысить сложность принудительно?",
        reply_markup=change_gif_keyboard
    )


@personal_accaunt_router.callback_query(F.data == "set-up-kn-level-force")
async def change_kn_level_up(query: CallbackQuery):
    user = get_user(query.message.chat.id)
    create_action("action_complicate_difficulty", user)


@personal_accaunt_router.callback_query(F.data == "set-down-kn-level")
async def change_kn_level_down(query: CallbackQuery):
    user = get_user(query.message.chat.id)
    create_action("action_simplify_difficulty", user)