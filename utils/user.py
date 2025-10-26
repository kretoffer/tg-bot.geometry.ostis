from sc_client.models import ScAddr, ScTemplate, ScLinkContent, ScLinkContentType
from sc_client.client import search_by_template, set_link_contents, erase_elements
from sc_client.constants import sc_type

from sc_kpm.sc_keynodes import ScKeynodes
from sc_kpm.utils import generate_connector


def change_user_class(user: ScAddr, user_class: str | int):
    templ = ScTemplate()
    templ.quintuple(
        user,
        sc_type.VAR_COMMON_ARC,
        (sc_type.VAR_NODE_LINK, "_link"),
        sc_type.VAR_PERM_POS_ARC,
        ScKeynodes.resolve("nrel_class", sc_type.CONST_NODE_NON_ROLE)
    )
    link = search_by_template(templ)[0].get("_link")
    content = ScLinkContent(str(user_class), ScLinkContentType.STRING, link)
    set_link_contents(content)


def clear_prefs(user: ScAddr):
    clear_set_by_attr(user, ScKeynodes.resolve("nrel_preferable_content_types", sc_type.CONST_NODE_NON_ROLE))


def clear_charects(user: ScAddr):
    clear_set_by_attr(user, ScKeynodes.resolve("nrel_personal_characteristics", sc_type.CONST_NODE_NON_ROLE))


def clear_set_by_attr(src: ScAddr, attr: ScAddr):
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
    search_results = search_by_template(templ)
    for res in search_results:
        erase_elements(res.get("_arc"))


def add_to_set_by_attr(src: ScAddr, attr: ScAddr, *addetable: ScAddr):
    templ = ScTemplate()
    templ.quintuple(
        src,
        sc_type.VAR_COMMON_ARC,
        (sc_type.VAR_NODE_TUPLE, "_set"),
        sc_type.VAR_PERM_POS_ARC,
        attr
    )
    node_set = search_by_template(templ)[0].get("_set")
    for el in addetable:
        generate_connector(sc_type.CONST_PERM_POS_ARC, node_set, el)


def add_perfs(user: ScAddr, *prefs: ScAddr):
    add_to_set_by_attr(user, ScKeynodes.resolve("nrel_preferable_content_types", sc_type.CONST_NODE_NON_ROLE), *prefs)


def add_charects(user: ScAddr, *charects: ScAddr):
    add_to_set_by_attr(user, ScKeynodes.resolve("nrel_personal_characteristics", sc_type.CONST_NODE_NON_ROLE), *charects)
