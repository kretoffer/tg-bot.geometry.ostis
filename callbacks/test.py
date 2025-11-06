from sc_async_client.constants import sc_type
from sc_async_client.models import ScAddr, ScTemplate
from sc_async_client.client import search_by_template

from sc_async_kpm.sc_keynodes import ScKeynodes
from sc_async_kpm.utils.action_utils import get_action_result
from sc_async_kpm.utils import get_link_content_data

from utils.get_user import get_user_passing_test_history, get_current_test
from utils.question import question_to_question_object
from utils.get_user import get_user_by_action
from utils.tests import get_last_question

from keyboards.diagnostc_test import get_question_keyboard

from create_bot import bot


async def get_next_question_callback(src: ScAddr, connector: ScAddr, trg: ScAddr):
    user, user_id = await get_user_by_action(trg)

    test = await get_current_test(user)
    question = await get_last_question(await get_user_passing_test_history(user, test))
    if not question.is_valid():
        return 

    templ = ScTemplate()
    templ.quintuple(
        question,
        sc_type.VAR_PERM_POS_ARC,
        (sc_type.VAR_NODE, "question"),
        sc_type.VAR_PERM_POS_ARC,
        await ScKeynodes.resolve("rrel_test_question", sc_type.VAR_NODE_ROLE)
    )
    question = (await search_by_template(templ))[0].get("question")

    if question.is_valid():
        question_info = await question_to_question_object(question)
        await bot.send_message(chat_id=user_id, text=question_info.text, parse_mode="markdown", reply_markup=get_question_keyboard(question_info))


async def finish_test_callback(src: ScAddr, connector: ScAddr, trg: ScAddr):
    user, user_id = await get_user_by_action(trg)
    result = await get_action_result(trg)
    templ = ScTemplate()
    templ.triple(
        result,
        sc_type.VAR_PERM_POS_ARC,
        (sc_type.VAR_NODE, "_kn_level")
    )
    templ.quintuple(
        "_kn_level",
        sc_type.VAR_COMMON_ARC,
        (sc_type.VAR_NODE_LINK, "_link"),
        sc_type.VAR_PERM_POS_ARC,
        await ScKeynodes.resolve("nrel_main_idtf", sc_type.CONST_NODE_NON_ROLE)
    )
    level = (await get_link_content_data((await search_by_template(templ))[0].get("_link"))).split()[0]
    await bot.send_message(chat_id=user_id, text=f"Тест завершен\nРезультат: {level}")
