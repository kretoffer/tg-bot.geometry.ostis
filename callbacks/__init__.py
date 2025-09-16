import logging
from logging import getLogger

from sc_client.constants import sc_type
from sc_client.models import ScAddr, ScTemplate
from sc_client.client import search_by_template

from sc_kpm.sc_keynodes import ScKeynodes

from callbacks.test import (
    get_next_question_callback,
    answered_question_callback
)


callbacks = {
    ScKeynodes.resolve("action_start_test", sc_type.CONST_NODE): get_next_question_callback,
    ScKeynodes.resolve("action_get_next_question", sc_type.CONST_NODE): get_next_question_callback,
    ScKeynodes.resolve("action_answered_test_question", sc_type.CONST_NODE): answered_question_callback
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


async def action_event_callback(src: ScAddr, connector: ScAddr, trg: ScAddr):
    print("action_event_callback")
    action_class = get_action_class(trg)
    if action_class in callbacks:
        await callbacks[action_class](src, connector, trg)
    else:
        logger.warning(f"Unprocessed class of action: {action_class}")