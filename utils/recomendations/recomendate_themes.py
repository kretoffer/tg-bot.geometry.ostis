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
    for i in ("other_themes", "good_themes", "bad_themes"):
        templ.quintuple(
            "struct",
            sc_type.VAR_PERM_POS_ARC,
            (sc_type.VAR_NODE, f"{i}_set"),
            sc_type.VAR_PERM_POS_ARC,
            ScKeynodes.resolve(f"rrel_{i}", sc_type.VAR_NODE_ROLE)
        )

    search_result = search_by_template(templ)[0]
    good_themes_set = search_result.get("good_themes_set")
    bad_themes_set = search_result.get("bad_themes_set")
    other_themes_set = search_result.get("other_themes_set")

    good_themes = list(ScSet(good_themes_set).elements_set)
    bad_themes = list(ScSet(bad_themes_set).elements_set)
    other_themes = list(ScSet(other_themes_set).elements_set)

    themes_recomendation = good_themes + other_themes + bad_themes
    return themes_recomendation
