from sc_async_client.constants import sc_type
from sc_async_client.models import ScTemplate, ScAddr
from sc_async_client.client import search_by_template
from sc_async_kpm import ScKeynodes

async def get_rating(user: ScAddr, relation: ScAddr) -> ScAddr:
    templ = ScTemplate()
    templ.quintuple(
        user,
        sc_type.COMMON_ARC,
        (sc_type.VAR_NODE_STRUCTURE, "_rating"),
        sc_type.VAR_PERM_POS_ARC,
        relation
    )

    search_results = await search_by_template(templ)
    if search_results:
        return search_results[0].get("_rating")
    return ScAddr()


async def get_self_rating(user: ScAddr) -> ScAddr:
    return await get_rating(user, await ScKeynodes.resolve("nrel_self_rating", sc_type.CONST_NODE_NON_ROLE))

async def get_system_rating(user: ScAddr) -> ScAddr:
    return await get_rating(user, await ScKeynodes.resolve("nrel_system_rating", sc_type.CONST_NODE_NON_ROLE))