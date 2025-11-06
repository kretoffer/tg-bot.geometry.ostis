import logging
from logging import getLogger

from sc_async_client.constants import sc_type
from sc_async_client.models import ScAddr, ScTemplate
from sc_async_client.client import search_by_template

from sc_async_kpm.sc_keynodes import ScKeynodes

from callbacks.test import (
    get_next_question_callback,
    finish_test_callback
)
from callbacks.recomendations import (
    generated_recomendations_for_study_callback,
    get_lesson_callback,
    get_lesson_no_callback,
    generated_recomendations_for_testing_or_solve_task_callback,
    get_test_callback,
    get_task_callback
)
from callbacks.auth import reg_user_callback
from callbacks.reflection import (
    show_progress_callback,
    simplify_callback,
    harderfy_callback,
    simplify_callback_no,
    harderfy_callback_no
)

callbacks = {}
no_callbacks = {}

async def init_callbacks():
    callbacks.update({
        await ScKeynodes.resolve("action_start_test", sc_type.CONST_NODE): get_next_question_callback,
        await ScKeynodes.resolve("action_get_next_question", sc_type.CONST_NODE): get_next_question_callback,
        await ScKeynodes.resolve("action_finish_test", sc_type.CONST_NODE): finish_test_callback,
        await ScKeynodes.resolve("action_form_theme_recommendations_for_user_to_study", sc_type.CONST_NODE): generated_recomendations_for_study_callback,
        await ScKeynodes.resolve("action_get_lesson_on_theme", sc_type.CONST_NODE): get_lesson_callback,

        await ScKeynodes.resolve("action_reg_user", sc_type.CONST_NODE): reg_user_callback,

        await ScKeynodes.resolve("action_form_theme_recommendations_for_user_to_solve_test_or_task", sc_type.CONST_NODE): generated_recomendations_for_testing_or_solve_task_callback,
        await ScKeynodes.resolve("action_form_test_recommendations_for_user", sc_type.CONST_NODE): get_test_callback,
        await ScKeynodes.resolve("action_form_task_recommendations_for_user", sc_type.CONST_NODE): get_task_callback,

        await ScKeynodes.resolve("action_show_progress", sc_type.CONST_NODE): show_progress_callback,
        await ScKeynodes.resolve("action_simplify_difficulty", sc_type.CONST_NODE): simplify_callback,
        await ScKeynodes.resolve("action_complicate_difficulty", sc_type.CONST_NODE): harderfy_callback
    })

    no_callbacks.update({
        await ScKeynodes.resolve("action_get_lesson_on_theme", sc_type.CONST_NODE): get_lesson_no_callback,

        await ScKeynodes.resolve("action_simplify_difficulty", sc_type.CONST_NODE): simplify_callback_no,
        await ScKeynodes.resolve("action_complicate_difficulty", sc_type.CONST_NODE): harderfy_callback_no
    })


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = getLogger("logger")


async def get_action_class(action: ScAddr) -> ScAddr:
    templ = ScTemplate()
    templ.triple(
        (sc_type.VAR_NODE, "action_class"),
        sc_type.VAR_PERM_POS_ARC,
        action
    )
    templ.triple(
        await ScKeynodes.resolve("action", sc_type.VAR_NODE_CLASS),
        sc_type.VAR_PERM_POS_ARC,
        "action_class"
    )
    if search_results := await search_by_template(templ):
        return search_results[0].get("action_class")


async def action_event_callback(src: ScAddr, connector: ScAddr, trg: ScAddr):
    action_class = await get_action_class(trg)
    if not callbacks:
        await init_callbacks()
    if action_class in callbacks:
        logger.info(f"Successfully action: {action_class}")
        await callbacks[action_class](src, connector, trg)
    else:
        logger.warning(f"Unprocessed class of successfully action: {action_class}")


async def action_event_no_callback(src: ScAddr, connector: ScAddr, trg: ScAddr):
    action_class = await get_action_class(trg)
    if not no_callbacks:
        await init_callbacks()
    if action_class in no_callbacks:
        logger.info(f"Unsuccessfully action: {action_class}")
        await no_callbacks[action_class](src, connector, trg)
    else:
        logger.warning(f"Unprocessed class of unsuccessfully action: {action_class}")
