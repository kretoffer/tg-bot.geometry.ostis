from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from keyboards.start_keyboards import start_without_test_keyboard

from config import START_PHRASE_WITHOUT_TEST

from utils.get_user import check_user_in_sc_machine, get_user
from utils.create_action import create_action
from utils.callback_filters import PrefixCallbackFilter

from sc_client.models import ScAddr
from sc_client.constants import sc_type

from sc_kpm.sc_keynodes import ScKeynodes


tests_router = Router()


@tests_router.message(Command("tests"))
@tests_router.message(Command("test"))
@tests_router.message(F.text.lower() in ("тест", "тесты"))
async def lessons_cmd(message: Message):
    if await check_user_in_sc_machine(message.from_user.id):
        await message.answer(START_PHRASE_WITHOUT_TEST, reply_markup=start_without_test_keyboard)

    user = get_user(message.from_user.id)
    create_action(
        "action_form_theme_recommendations_for_user_to_solve_test_or_task",
        user,
        ScKeynodes.resolve("test_recommendations", sc_type.VAR_NODE)
    )


@tests_router.callback_query(PrefixCallbackFilter("test-theme"))
async def select_lesson_theme(query: CallbackQuery):
    theme_addr = int(query.data.split(":")[1])
    theme = ScAddr(theme_addr)

    user = get_user(query.message.chat.id)

    create_action("action_form_test_recommendations_for_user", user, theme)
