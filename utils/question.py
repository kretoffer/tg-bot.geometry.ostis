from sc_async_client.constants import sc_type
from sc_async_client.models import ScAddr, ScTemplate
from sc_async_client.client import search_by_template

from sc_async_kpm.sc_keynodes import ScKeynodes
from sc_async_kpm.utils import get_link_content_data

from shemes.question import Question

from utils.get_idtf import search_lang_value_by_nrel_identifier

async def question_to_question_object(question: ScAddr) -> Question:
    answers = []
    templ = ScTemplate()
    templ.quintuple(
        question,
        sc_type.VAR_COMMON_ARC,
        (sc_type.VAR_NODE, "answer"),
        sc_type.VAR_PERM_POS_ARC,
        await ScKeynodes.resolve("nrel_possible_answer", sc_type.CONST_NODE_NON_ROLE)
    )
    search_results = await search_by_template(templ)
    for el in search_results:
        answer = el.get("answer")
        answers.append((
            answer,
            await get_link_content_data(await search_lang_value_by_nrel_identifier(answer, "nrel_text"))
        ))
    return Question(
        await get_link_content_data(await search_lang_value_by_nrel_identifier(question, "nrel_condition")),
        answers
    )