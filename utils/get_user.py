from sc_client.constants import sc_type
from sc_client.models import ScTemplate, ScLinkContent, ScLinkContentType, ScConstruction, ScAddr
from sc_client.client import search_by_template, create_elements

from sc_kpm import ScKeynodes


def get_user(user_id: int) -> ScAddr:
    constr = ScConstruction()
    constr.generate_link(sc_type.CONST_NODE_LINK, ScLinkContent(user_id, ScLinkContentType.INT))
    link_user_id = create_elements(constr)[0]
    templ = ScTemplate()
    templ.quintuple(
        (sc_type.VAR_NODE, "user"),
        sc_type.VAR_COMMON_ARC,
        link_user_id,
        sc_type.VAR_PERM_POS_ARC,
        ScKeynodes.resolve("nrel_tg_id", sc_type.NODE_NON_ROLE)
    )
    if search_results := search_by_template(templ):
        return search_results[0].get("user")
    return ScAddr()