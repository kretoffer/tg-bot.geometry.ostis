from sc_client.constants import sc_type
from sc_client.models import ScTemplate, ScAddr
from sc_client.client import search_by_template, delete_elements

from sc_kpm import ScKeynodes

from typing import List


def get_themes_from_set(set: ScAddr) -> List[ScAddr]:
    templ = ScTemplate()
    templ.triple(
        set,
        sc_type.VAR_PERM_POS_ARC,
        (sc_type.VAR_NODE, "theme")
    )
    search_results = search_by_template(templ)

    themes = []
    for el in search_results:
        themes.append(el.get("theme"))
    return themes


async def get_themes_list() -> List[ScAddr]:
    templ = ScTemplate()
    templ.triple(
        ScKeynodes.resolve("concept_theme", sc_type.CONST_NODE_CLASS),
        sc_type.VAR_PERM_POS_ARC,
        (sc_type.VAR_NODE, "theme")
    )
    search_results = search_by_template(templ)

    themes = []
    for search_result in search_results:
        themes.append(search_result.get("theme"))
    return themes


def get_worth_studied_themes_set(rating: ScAddr, user: ScAddr) -> ScAddr:
    return get_studied_themes_set(rating, user, ScKeynodes.resolve("nrel_worth_studied_themes", sc_type.CONST_NODE_NON_ROLE))


def get_well_studied_themes_set(rating: ScAddr, user: ScAddr) -> ScAddr:
    return get_studied_themes_set(rating, user, ScKeynodes.resolve("nrel_well_studied_themes", sc_type.CONST_NODE_NON_ROLE))


def get_studied_themes_set(rating: ScAddr, user: ScAddr, comporator) -> ScAddr:
    templ = ScTemplate()
    templ.quintuple(
        user,
        sc_type.VAR_COMMON_ARC,
        (sc_type.VAR_NODE_TUPLE, "themes"),
        sc_type.VAR_PERM_POS_ARC,
        comporator
    )
    templ.triple(
        rating,
        sc_type.VAR_PERM_POS_ARC,
        "themes"
    )
    studied_themes_set = search_by_template(templ)[0].get("themes")
    return studied_themes_set


def delete_themes_from_set(tuple: ScAddr, set: ScAddr):
    templ = ScTemplate()
    templ.quintuple(
        tuple,
        (sc_type.VAR_PERM_POS_ARC, "arc_to_theme"),
        (sc_type.VAR_NODE, "theme"),
        sc_type.VAR_PERM_POS_ARC,
        set
    )
    templ.triple(
        set,
        (sc_type.VAR_PERM_POS_ARC, "arc_from_set"),
        "theme"
    )
    search_results = search_by_template(templ)
    for search_result in search_results:
        delete_elements(search_result.get("arc_to_theme"), search_result.get("arc_from_set"))
