from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from utils.callback_filters import PrefixCallbackFilter
from utils.get_user import get_user, get_current_test
from utils.create_action import create_action

from sc_client.constants import sc_type
from sc_client.models import ScAddr, ScTemplate, ScLinkContentType
from sc_client.client import search_by_template

from sc_kpm.sc_keynodes import ScKeynodes
from sc_kpm.utils import generate_link

from keyboards.diagnostc_test import reg_classes_keyboard, get_reg_knowledge_level_keyboard

diagnostic_test_router = Router()


async def set_answer(user: ScAddr, test: ScAddr, answer: ScAddr):
    "Запись ответа пользователя в БЗ"
    if not test.is_valid():
        return
    create_action("action_answered_test_question", user, test, answer)


@diagnostic_test_router.message(F.text.lower() == "пройти тест")
@diagnostic_test_router.message(Command("test"))
async def cmd_start_diagnostic_test(message: Message):
    user = get_user(message.chat.id)
    if user:
        await start_diagnostic_test(user)
    else:
        await message.answer("Выберите класс:", reply_markup=reg_classes_keyboard)


@diagnostic_test_router.callback_query(PrefixCallbackFilter("user-reg-class"))
async def set_user_class(query: CallbackQuery):
    user_class = query.data.split(":")[1]
    await query.message.edit_text("Выберите свой уровень знаний:", reply_markup=get_reg_knowledge_level_keyboard(user_class))


@diagnostic_test_router.callback_query(PrefixCallbackFilter("user-reg-kn-level"))
async def set_user_kn_level(query: CallbackQuery):
    [_, user_class, kn_level] = query.data.split(":")

    link_user_id = generate_link(str(query.message.chat.id), ScLinkContentType.STRING, sc_type.CONST_NODE_LINK)
    user_class_link = generate_link(user_class, ScLinkContentType.STRING, sc_type.CONST_NODE_LINK)
    user_name_link = generate_link(query.message.chat.first_name, ScLinkContentType.STRING, sc_type.CONST_NODE_LINK)
    user_kn_level_link = ScKeynodes.resolve(f"{kn_level}_knowledge_level", sc_type.CONST_NODE)

    await query.message.delete()

    create_action("action_reg_user", link_user_id, user_class_link, user_name_link, user_kn_level_link)


async def get_last_question(passing_test_history: ScAddr) -> ScAddr:
    if not passing_test_history.is_valid():
        return ScAddr()
    templ = ScTemplate()
    templ.quintuple(
        passing_test_history,
        sc_type.VAR_PERM_POS_ARC,
        (sc_type.VAR_NODE, "question"),
        sc_type.VAR_PERM_POS_ARC,
        ScKeynodes.resolve("rrel_last", sc_type.CONST_NODE_ROLE)
    )
    question = search_by_template(templ)[0].get("question")
    return question


@diagnostic_test_router.callback_query(PrefixCallbackFilter("test_answer"))
async def answer_to_question(query: CallbackQuery):
    answer_sc_addr = int(query.data.split(":")[1])
    user = get_user(query.message.chat.id)
    test = await get_current_test(user)
    answer = await ScAddr(answer_sc_addr)

    await set_answer(user, test, answer)

    await query.message.delete()
