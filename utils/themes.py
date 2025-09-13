from sc_client.constants import sc_type
from sc_client.models import ScTemplate, ScAddr
from sc_client.client import search_by_template

from sc_kpm import ScKeynodes
from sc_kpm.utils import get_link_content_data

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

def get_name_of_theme(theme: ScAddr) -> str:
    templ = ScTemplate()
    templ.quintuple(
            theme,
            sc_type.VAR_COMMON_ARC,
            (sc_type.VAR_NODE_LINK, "name"),
            sc_type.VAR_PERM_POS_ARC,
            ScKeynodes.resolve("nrel_name", sc_type.CONST_NODE_NON_ROLE)
        )
    name = str(get_link_content_data(search_by_template(templ)[0].get("name")))
    return name


async def get_themes_list() -> list:
    ... # TODO получение списка тем из БЗ
    return [f"theme {i}" for i in range(1, 51)] # заглушка


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
