from sc_async_client.constants import sc_type
from sc_async_client.models import ScAddr, ScTemplate
from sc_async_client.client import search_by_template

from sc_async_kpm.sc_keynodes import ScKeynodes

from utils.create_action import create_action


async def reg_user_callback(src: ScAddr, connector: ScAddr, trg: ScAddr):
    templ = ScTemplate()
    templ.quintuple(
        trg,
        sc_type.VAR_PERM_POS_ARC,
        (sc_type.VAR_NODE_LINK, "user_id"),
        sc_type.VAR_PERM_POS_ARC,
        await ScKeynodes.rrel_index(1)
    )
    templ.quintuple(
        (sc_type.VAR_NODE, "user"),
        sc_type.VAR_COMMON_ARC,
        "user_id",
        sc_type.VAR_PERM_POS_ARC,
        await ScKeynodes.resolve("nrel_tg_id", sc_type.VAR_NODE_NON_ROLE)
    )
    search_result = (await search_by_template(templ))[0]
    user = search_result.get("user")
    await create_action("action_start_diagnostic_test", user)