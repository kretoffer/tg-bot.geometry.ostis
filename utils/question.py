from sc_client.constants import sc_type
from sc_client.models import ScAddr, ScTemplate
from sc_client.client import search_by_template

from sc_kpm.sc_keynodes import ScKeynodes
from sc_kpm.utils import get_link_content_data

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
        ScKeynodes.resolve("nrel_possible_answer", sc_type.CONST_NODE_NON_ROLE)
    )
    search_results = search_by_template(templ)
    for el in search_results:
        answer = el.get("answer")
        answers.append((
            answer,
            get_link_content_data(search_lang_value_by_nrel_identifier(answer, "nrel_text"))
        ))
    return Question(
        get_link_content_data(search_lang_value_by_nrel_identifier(question, "nrel_condition")),
        answers
    )