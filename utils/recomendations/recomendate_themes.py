from sc_client.models import ScAddr, ScTemplate
from sc_client.constants import sc_type
from sc_client.client import search_by_template

from sc_kpm.sc_keynodes import ScKeynodes
from sc_kpm.sc_sets import ScSet

from typing import List


async def get_recomendate_themes(*, data: str = None, result: ScAddr = None, **kwargs) -> List[ScAddr]:
    if not result:
        result_addr = int(data.split(":")[3])
        result = ScAddr(result_addr)

    templ = ScTemplate()
    templ.triple(
        result,
        sc_type.VAR_PERM_POS_ARC,
        (sc_type.VAR_NODE_STRUCTURE, "set")
    )
    templ.triple(
        "set",
        sc_type.VAR_PERM_POS_ARC,
        (sc_type.VAR_NODE, "struct")
    )
    templ.quintuple(
        "struct",
        sc_type.VAR_PERM_POS_ARC,
        (sc_type.VAR_NODE, "other_themes_set"),
        sc_type.VAR_PERM_POS_ARC,
        ScKeynodes.resolve("rrel_other_themes", sc_type.VAR_NODE_ROLE)
    )
    search_result = search_by_template(templ)[0]
    other_themes_set = search_result.get("other_themes_set")
    templ.triple_list = templ.triple_list[:-2]
    templ.quintuple(
        "struct",
        sc_type.VAR_PERM_POS_ARC,
        (sc_type.VAR_NODE, "good_themes_set"),
        sc_type.VAR_PERM_POS_ARC,
        ScKeynodes.resolve("rrel_good_themes", sc_type.VAR_NODE_ROLE)
    )

    search_result = search_by_template(templ)[0]
    good_themes_set = search_result.get("good_themes_set")

    good_themes = list(ScSet(set_node=good_themes_set).elements_set)
    other_themes = list(ScSet(set_node=other_themes_set).elements_set)

    themes_recomendation = good_themes + other_themes

    templ.quintuple(
        "struct",
        sc_type.VAR_PERM_POS_ARC,
        (sc_type.VAR_NODE, "bad_themes_set"),
        sc_type.VAR_PERM_POS_ARC,
        ScKeynodes.resolve("rrel_bad_themes", sc_type.VAR_NODE_ROLE)
    )

    if search_results := search_by_template(templ):
        bad_themes_set = search_results[0].get("bad_themes_set")
        bad_themes = list(ScSet(set_node=bad_themes_set).elements_set)
        themes_recomendation += bad_themes

    return themes_recomendation
