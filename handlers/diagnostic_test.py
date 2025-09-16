from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from shemes.question import Question

from utils.callback_filters import PrefixCallbackFilter
from utils.get_user import get_user, get_current_test
from utils.create_action import create_action

from sc_client.constants import sc_type
from sc_client.models import ScAddr, ScTemplate
from sc_client.client import search_by_template

from sc_kpm.sc_keynodes import ScKeynodes

diagnostic_test_router = Router()


async def set_answer(user: ScAddr, test: ScAddr, answer: ScAddr):
    "Запись ответа пользователя в БЗ"
    if not test.is_valid():
        return
    await create_action("action_answered_test_question", user, test, answer)


@diagnostic_test_router.message(F.text.lower() == "пройти тест")
@diagnostic_test_router.message(Command("test"))
async def cmd_start_diagnostic_test(message: Message):
    user = get_user(message.from_user.id)
    
    await create_action("action_start_test", user)


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
