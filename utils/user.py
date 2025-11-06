from sc_async_client.models import ScAddr, ScTemplate, ScLinkContent, ScLinkContentType
from sc_async_client.client import search_by_template, set_link_contents, erase_elements
from sc_async_client.constants import sc_type

from sc_async_kpm.sc_keynodes import ScKeynodes
from sc_async_kpm.utils import generate_connector


async def change_user_class(user: ScAddr, user_class: str | int):
    templ = ScTemplate()
    templ.quintuple(
        user,
        sc_type.VAR_COMMON_ARC,
        (sc_type.VAR_NODE_LINK, "_link"),
        sc_type.VAR_PERM_POS_ARC,
        await ScKeynodes.resolve("nrel_class", sc_type.CONST_NODE_NON_ROLE)
    )
    link = (await search_by_template(templ))[0].get("_link")
    content = ScLinkContent(str(user_class), ScLinkContentType.STRING, link)
    await set_link_contents(content)


async def clear_prefs(user: ScAddr):
    await clear_set_by_attr(user, await ScKeynodes.resolve("nrel_preferable_content_types", sc_type.CONST_NODE_NON_ROLE))


async def clear_charects(user: ScAddr):
    await clear_set_by_attr(user, await ScKeynodes.resolve("nrel_personal_characteristics", sc_type.CONST_NODE_NON_ROLE))


async def clear_set_by_attr(src: ScAddr, attr: ScAddr):
    templ = ScTemplate()
    templ.quintuple(
        src,
        sc_type.VAR_COMMON_ARC,
        (sc_type.VAR_NODE_TUPLE, "_set"),
        sc_type.VAR_PERM_POS_ARC,
        attr
    )
    templ.triple(
        "_set",
        (sc_type.VAR_PERM_POS_ARC, "_arc"),
        sc_type.VAR_NODE
    )
    search_results = await search_by_template(templ)
    for res in search_results:
        await erase_elements(res.get("_arc"))


async def add_to_set_by_attr(src: ScAddr, attr: ScAddr, *addetable: ScAddr):
    templ = ScTemplate()
    templ.quintuple(
        src,
        sc_type.VAR_COMMON_ARC,
        (sc_type.VAR_NODE_TUPLE, "_set"),
        sc_type.VAR_PERM_POS_ARC,
        attr
    )
    node_set = (await search_by_template(templ))[0].get("_set")
    for el in addetable:
        await generate_connector(sc_type.CONST_PERM_POS_ARC, node_set, el)


async def add_perfs(user: ScAddr, *prefs: ScAddr):
    await add_to_set_by_attr(user, await ScKeynodes.resolve("nrel_preferable_content_types", sc_type.CONST_NODE_NON_ROLE), *prefs)


async def add_charects(user: ScAddr, *charects: ScAddr):
    await add_to_set_by_attr(user, await ScKeynodes.resolve("nrel_personal_characteristics", sc_type.CONST_NODE_NON_ROLE), *charects)
