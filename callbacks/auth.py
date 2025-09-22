from sc_client.constants import sc_type
from sc_client.models import ScAddr, ScTemplate
from sc_client.client import search_by_template

from sc_kpm.sc_keynodes import ScKeynodes

from utils.create_action import create_action


async def reg_user_callback(src: ScAddr, connector: ScAddr, trg: ScAddr):
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
    create_action("action_start_test", user)