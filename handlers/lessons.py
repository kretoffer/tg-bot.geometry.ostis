from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from sc_client.models import ScAddr

from keyboards.start_keyboards import start_without_test_keyboard
from keyboards.lessons import get_lesson_message_markup

from config import START_PHRASE_WITHOUT_TEST

from utils.get_user import check_user_in_sc_machine, get_user
from utils.create_action import create_action
from utils.callback_filters import PrefixCallbackFilter
from utils.send_message_with_content import send_message_with_content

from sc_kpm.utils import get_link_content_data

from handlers.personal_account import cmd_accaunt


lessons_router = Router()


@lessons_router.message(Command("lessons"))
@lessons_router.message(Command("lesson"))
@lessons_router.message(lambda msg: msg.text.lower() in ("уроки", "урок"))
async def lessons_cmd(message: Message):
    if await check_user_in_sc_machine(message.from_user.id):
        await message.answer(START_PHRASE_WITHOUT_TEST, reply_markup=start_without_test_keyboard)

    user = get_user(message.from_user.id)
    create_action("action_form_theme_recommendations_for_user_to_study", user)


@lessons_router.callback_query(PrefixCallbackFilter("lesson-theme"))
async def select_lesson_theme(query: CallbackQuery):
    theme_addr = int(query.data.split(":")[1])
    theme = ScAddr(theme_addr)

    user = get_user(query.message.chat.id)

    create_action("action_get_lesson_on_theme", user, theme)


@lessons_router.callback_query(PrefixCallbackFilter("lesson-message"))
async def lesson_message(query: CallbackQuery, bot: Bot):
    message_addr = int(query.data.split(":")[1])
    message = ScAddr(message_addr)

    markup = get_lesson_message_markup(message)

    content = get_link_content_data(message)
    await send_message_with_content(query.message.chat.id, content, bot, markup)
    await query.message.delete()


@lessons_router.callback_query(F.data == "finish-lesson")
async def start_reflection(query: CallbackQuery):
    cmd_accaunt(message=query.message)
    query.message.delete()