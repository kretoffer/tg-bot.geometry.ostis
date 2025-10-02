from utils.create_action import create_action

from sc_client.models import ScAddr, ScTemplate
from sc_client.constants import sc_type
from sc_client.client import search_by_template

from sc_kpm.sc_keynodes import ScKeynodes


async def set_answer(user: ScAddr, test: ScAddr, answer: ScAddr):
    "Запись ответа пользователя в БЗ"
    if not test.is_valid():
        return
    create_action("action_answered_test_question", user, test, answer)


async def get_last_question(passing_test_history: ScAddr) -> ScAddr:
    if not passing_test_history.is_valid():
        return ScAddr()
    templ = ScTemplate()
    templ.quintuple(
        passing_test_history,
        sc_type.VAR_PERM_POS_ARC,
        (sc_type.VAR_NODE, "question"),
        sc_type.VAR_ACTUAL_TEMP_POS_ARC,
        ScKeynodes.resolve("rrel_last", sc_type.CONST_NODE_ROLE)
    )
    if search_results := search_by_template(templ):
        question = search_results[0].get("question")
        return question
    return ScAddr()