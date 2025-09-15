import logging
from logging import getLogger

from sc_client.constants import sc_type
from sc_client.models import ScAddr, ScTemplate
from sc_client.client import search_by_template

from sc_kpm.sc_keynodes import ScKeynodes


callbacks = {

}

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = getLogger("logger")


def get_action_class(action: ScAddr) -> ScAddr:
    templ = ScTemplate()
    templ.triple(
        (sc_type.VAR_NODE_CLASS, "action_class"),
        sc_type.VAR_PERM_POS_ARC,
        action
    )
    if search_results := search_by_template(templ):
        print(search_results)
        return search_results[0].get("action_class")


def action_event_callback(src: ScAddr, connector: ScAddr, trg: ScAddr):
    action_class = get_action_class(src)
    if action_class in callbacks:
        callbacks[action_class](src, connector, trg)
    else:
        logger.warning(f"Unprocessed class of action: {action_class}")