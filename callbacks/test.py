from sc_client.constants import sc_type
from sc_client.models import ScAddr, ScTemplate
from sc_client.client import search_by_template

from sc_kpm.sc_keynodes import ScKeynodes
from sc_kpm.utils import get_link_content_data

from create_bot import bot

from utils.get_user import get_user_passing_test_history, get_current_test
from utils.question import question_to_question_object
from utils.create_action import create_action

from handlers.diagnostic_test import get_last_question

from keyboards.diagnostc_test import get_question_keyboard


async def get_next_question_callback(src: ScAddr, connector: ScAddr, trg: ScAddr):
    print("get_next_question_callback")
    templ = ScTemplate()
    templ.quintuple(
        trg,
        sc_type.VAR_PERM_POS_ARC,
        (sc_type.VAR_NODE, "user"),
        sc_type.VAR_PERM_POS_ARC,
        ScKeynodes.rrel_index(1)
    )
    templ.quintuple(
        "user",
        sc_type.VAR_COMMON_ARC,
        (sc_type.VAR_NODE_LINK, "user_id"),
        sc_type.VAR_PERM_POS_ARC,
        ScKeynodes.resolve("nrel_tg_id", sc_type.VAR_NODE_NON_ROLE)
    )
    search_result = search_by_template(templ)[0]
    user = search_result.get("user")
    user_id = get_link_content_data(search_result.get("user_id"))

    test = await get_current_test(user)
    question = await get_last_question(get_user_passing_test_history(user, test))
    if question.is_valid():
        question_info = await question_to_question_object(question)
        await bot.send_message(user_id, question_info.text, parse_mode="markdown", reply_markup=get_question_keyboard(question_info))
    await bot.send_message(user_id, "Тест завершен")


async def answered_question_callback(src: ScAddr, connector: ScAddr, trg: ScAddr):
    templ = ScTemplate()
    templ.quintuple(
        src,
        sc_type.VAR_PERM_POS_ARC,
        (sc_type.VAR_NODE, "user"),
        sc_type.VAR_PERM_POS_ARC,
        ScKeynodes.rrel_index(1)
    )
    search_result = search_by_template(templ)[0]
    user = search_result.get("user")
    test = get_current_test(user)
    question = get_last_question(get_user_passing_test_history(user), test)
    await create_action("action_get_next_question", user, test, question)