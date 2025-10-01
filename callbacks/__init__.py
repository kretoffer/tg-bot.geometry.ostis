import logging
from logging import getLogger

import asyncio

from sc_client.constants import sc_type
from sc_client.models import ScAddr, ScTemplate
from sc_client.client import search_by_template

from sc_kpm.sc_keynodes import ScKeynodes

from callbacks.test import (
    get_next_question_callback,
    finish_test_callback
)
from callbacks.recomendations import (
    generated_recomendations_for_study_callback,
    get_lesson_callback,
    generated_recomendations_for_testing_or_solve_task_callback,
    get_test_callback,
    get_task_callback
)
from callbacks.auth import reg_user_callback


callbacks = {
    ScKeynodes.resolve("action_start_test", sc_type.CONST_NODE): get_next_question_callback,
    ScKeynodes.resolve("action_get_next_question", sc_type.CONST_NODE): get_next_question_callback,
    ScKeynodes.resolve("action_finish_test", sc_type.CONST_NODE): finish_test_callback,
    ScKeynodes.resolve("action_form_theme_recommendations_for_user_to_study", sc_type.CONST_NODE): generated_recomendations_for_study_callback,
    ScKeynodes.resolve("action_get_lesson_on_theme", sc_type.CONST_NODE): get_lesson_callback,
    ScKeynodes.resolve("action_reg_user", sc_type.CONST_NODE): reg_user_callback,
    ScKeynodes.resolve("action_form_theme_recommendations_for_user_to_solve_test_or_task", sc_type.CONST_NODE): generated_recomendations_for_testing_or_solve_task_callback,
    ScKeynodes.resolve("action_form_test_recommendations_for_user", sc_type.CONST_NODE): get_test_callback,
    ScKeynodes.resolve("action_form_task_recommendations_for_user", sc_type.CONST_NODE): get_task_callback
}


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = getLogger("logger")


def get_action_class(action: ScAddr) -> ScAddr:
    templ = ScTemplate()
    templ.triple(
        (sc_type.VAR_NODE, "action_class"),
        sc_type.VAR_PERM_POS_ARC,
        action
    )
    templ.triple(
        ScKeynodes.resolve("action", sc_type.VAR_NODE_CLASS),
        sc_type.VAR_PERM_POS_ARC,
        "action_class"
    )
    if search_results := search_by_template(templ):
        return search_results[0].get("action_class")


def action_event_callback(src: ScAddr, connector: ScAddr, trg: ScAddr):
    action_class = get_action_class(trg)
    if action_class in callbacks:
        logger.info(f"Action: {action_class}")
        asyncio.run(callbacks[action_class](src, connector, trg))
    else:
        logger.warning(f"Unprocessed class of action: {action_class}")
