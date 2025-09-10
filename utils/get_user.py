from sc_client.constants import sc_type
from sc_client.models import ScTemplate, ScLinkContent, ScLinkContentType, ScConstruction, ScAddr
from sc_client.client import search_by_template, create_elements

from sc_kpm import ScKeynodes
from sc_kpm.utils import get_link_content_data

from utils.get_rating import get_self_rating, get_system_rating
from utils.themes import get_themes_from_set, get_name_of_theme
from shemes.user import User, Rating

from typing import Optional, List


def get_user(user_id: int) -> ScAddr:
    # не работает, т.к. создает новый линк, а не находит старый
    constr = ScConstruction()
    constr.generate_link(sc_type.CONST_NODE_LINK, ScLinkContent(str(user_id), ScLinkContentType.STRING))
    link_user_id = create_elements(constr)[0]
    templ = ScTemplate()
    templ.quintuple(
        (sc_type.VAR_NODE, "user"),
        sc_type.VAR_COMMON_ARC,
        link_user_id,
        sc_type.VAR_PERM_POS_ARC,
        ScKeynodes.resolve("nrel_tg_id", sc_type.NODE_NON_ROLE)
    )
    print(search_by_template(templ))
    if search_results := search_by_template(templ):
        print(search_results)
        return search_results[0].get("user")
    return ScAddr()


def get_rating(rating: ScAddr) -> Optional[Rating]:
    if not rating.is_valid():
        return None
    templ = ScTemplate()
    templ.quintuple(
        (sc_type.VAR_NODE, "_knowledge_level_info"),
        sc_type.VAR_ACTUAL_TEMP_POS_ARC,
        rating,
        sc_type.VAR_PERM_POS_ARC,
        ScKeynodes("rrel_student", sc_type.CONST_NODE_ROLE)
    )

    templ.quintuple(
        "_knowledge_level_info",
        (sc_type.VAR_ACTUAL_TEMP_POS_ARC, "_arc_to_knowledge_level"),
        (sc_type.VAR_NODE, "_knowledge_level"),
        sc_type.VAR_PERM_POS_ARC,
        ScKeynodes("rrel_knowledge_level", sc_type.CONST_NODE_ROLE)
    )
    knowledge_level = None
    if search_results := search_by_template(templ):
        # TODO Получение уровня знаний в формате str
        ...

    templ.quintuple(
        rating,
        sc_type.VAR_COMMON_ARC,
        (sc_type.VAR_NODE, "themes"),
        sc_type.VAR_PERM_POS_ARC,
        ScKeynodes("nrel_worth_studied_themes", sc_type.CONST_NODE_NON_ROLE)
    )
    worth_studied_themes_set = search_by_template(templ)[0].get("themes")
    templ.quintuple(
        rating,
        sc_type.VAR_COMMON_ARC,
        (sc_type.VAR_NODE, "themes"),
        sc_type.VAR_PERM_POS_ARC,
        ScKeynodes("nrel_well_studied_themes", sc_type.CONST_NODE_NON_ROLE)
    )
    well_studied_themes_set = search_by_template(templ)[0].get("themes")
    worth_studied_themes = [get_name_of_theme(theme) for theme in get_themes_from_set(worth_studied_themes_set)]
    well_studied_themes = [get_name_of_theme(theme) for theme in get_themes_from_set(well_studied_themes_set)]


    return Rating(
        knowledge_level,
        worth_studied_themes,
        well_studied_themes
    )


def get_user_info(user_id: int) -> Optional[User]:
    user = get_user(user_id)
    if not user.is_valid():
        return None
    templ = ScTemplate()
    templ.quintuple(
        user,
        sc_type.VAR_COMMON_ARC,
        (sc_type.VAR_NODE_LINK, "name"),
        sc_type.VAR_PERM_POS_ARC,
        ScKeynodes.resolve("nrel_name", sc_type.NODE_NON_ROLE)
    )
    name = str(get_link_content_data(search_by_template(templ)[0].get("name")))
    templ.quintuple(
        user,
        sc_type.VAR_COMMON_ARC,
        (sc_type.VAR_NODE_LINK, "class"),
        sc_type.VAR_PERM_POS_ARC,
        ScKeynodes.resolve("nrel_class", sc_type.NODE_NON_ROLE)
    )
    user_class = int(get_link_content_data(search_by_template(templ)[0].get("class")))

    achievements = ...
    achievements = [] #Заглушка, пока не реализован класс Achievements
    return User(
        user_id,
        name,
        user_class,
        achievements,
        get_rating(get_self_rating(user)),
        get_rating(get_system_rating(user))
    )