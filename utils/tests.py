from utils.create_action import create_action

from sc_async_client.models import ScAddr, ScTemplate
from sc_async_client.constants import sc_type
from sc_async_client.client import search_by_template

from sc_async_kpm.sc_keynodes import ScKeynodes


async def set_answer(user: ScAddr, test: ScAddr, answer: ScAddr):
    "Запись ответа пользователя в БЗ"
    if not test.is_valid():
        return
    await create_action("action_answered_test_question", user, test, answer)


async def get_last_question(passing_test_history: ScAddr) -> ScAddr:
    if not passing_test_history.is_valid():
        return ScAddr()
    templ = ScTemplate()
    templ.quintuple(
        passing_test_history,
        sc_type.VAR_PERM_POS_ARC,
        (sc_type.VAR_NODE, "question"),
        sc_type.VAR_PERM_POS_ARC,
        await ScKeynodes.resolve("rrel_last", sc_type.CONST_NODE_ROLE)
    )
    if search_results := await search_by_template(templ):
        question = search_results[0].get("question")
        return question
    return ScAddr()