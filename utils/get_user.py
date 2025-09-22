from sc_client.constants import sc_type
from sc_client.models import ScTemplate, ScAddr
from sc_client.client import search_by_template, search_links_by_contents

from sc_kpm import ScKeynodes
from sc_kpm.utils import get_link_content_data

from utils.get_rating import get_self_rating, get_system_rating
from utils.themes import get_themes_from_set, get_well_studied_themes_set, get_worth_studied_themes_set
from utils.get_idtf import get_ru_main_identifier, get_name_str, get_description_str
from shemes.user import User, Rating, Achievement

from typing import Optional, List


def get_user(user_id: int) -> ScAddr:
    [searc_result] = search_links_by_contents(str(user_id))
    if searc_result:
        [link_user_id] = searc_result
    else:
        return ScAddr()
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


def get_rating(rating: ScAddr, user: ScAddr) -> Optional[Rating]:
    if not rating.is_valid():
        return None
    templ = ScTemplate()
    templ.quintuple(
        ScKeynodes.resolve("nrel_user_knowledge_level", sc_type.CONST_NODE_NON_ROLE),
        sc_type.VAR_ACTUAL_TEMP_POS_ARC,
        (sc_type.VAR_NODE, "main"),
        sc_type.VAR_PERM_POS_ARC,
        rating
    )
    templ.quintuple(
        "main",
        sc_type.VAR_ACTUAL_TEMP_POS_ARC,
        (sc_type.VAR_NODE, "knowledge_level"),
        sc_type.VAR_PERM_POS_ARC,
        ScKeynodes.resolve("rrel_knowledge_level", sc_type.CONST_NODE_ROLE)
    )
    knowledge_level = None
    if search_results := search_by_template(templ):
        knowledge_level_node = search_results[0].get("knowledge_level")
        knowledge_level = get_link_content_data(get_ru_main_identifier(knowledge_level_node))
    else: 
        return 

    worth_studied_themes_set = get_worth_studied_themes_set(rating, user)
    well_studied_themes_set = get_well_studied_themes_set(rating, user)
    worth_studied_themes = [get_name_str(theme) for theme in get_themes_from_set(worth_studied_themes_set)]
    well_studied_themes = [get_name_str(theme) for theme in get_themes_from_set(well_studied_themes_set)]


    return Rating(
        knowledge_level,
        worth_studied_themes,
        well_studied_themes
    )


def get_user_achievements(user: ScAddr) -> List[ScAddr]:
    templ = ScTemplate()
    templ.quintuple(
        user,
        sc_type.VAR_COMMON_ARC,
        (sc_type.VAR_NODE, "achievement"),
        sc_type.VAR_PERM_POS_ARC,
        ScKeynodes.resolve("nrel_achievements", sc_type.CONST_NODE_NON_ROLE)
    )
    search_results = search_by_template(templ)
    return [search_result.get("achievement") for search_result in search_results]


def get_user_achievements_info(achievements: List[ScAddr]) -> List[Achievement]:
    return [
        Achievement(
            get_name_str(achievement),
            get_description_str(achievement)
        )
        for achievement in achievements
    ]


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

    achievements = get_user_achievements(user)
    
    achievements = [] #Заглушка, пока не реализован класс Achievements
    return User(
        user_id,
        name,
        user_class,
        achievements,
        get_rating(get_self_rating(user), user),
        get_rating(get_system_rating(user), user)
    )


async def check_user_in_sc_machine(user_id: int) -> bool:
    if user := get_user(user_id):
        rating = get_system_rating(user)
        templ = ScTemplate()
        templ.quintuple(
            ScKeynodes.resolve("nrel_user_knowledge_level", sc_type.CONST_NODE_NON_ROLE),
            sc_type.VAR_ACTUAL_TEMP_POS_ARC,
            (sc_type.VAR_NODE, "main"),
            sc_type.VAR_PERM_POS_ARC,
            rating
        )
        templ.quintuple(
            "main",
            sc_type.VAR_ACTUAL_TEMP_POS_ARC,
            (sc_type.VAR_NODE, "knowledge_level"),
            sc_type.VAR_PERM_POS_ARC,
            ScKeynodes.resolve("rrel_knowledge_level", sc_type.CONST_NODE_ROLE)
        )
        if search_by_template(templ):
            return True
    return False


async def get_reflection_results(user_id: int):
    # TODO Получение результатов рефлексии
    return "Результаты рефлексии"


def get_user_passing_test_history(user: ScAddr, test: ScAddr) -> ScAddr:
    if not all((user, test)):
        return ScAddr()
    templ = ScTemplate()
    templ.quintuple(
        (sc_type.VAR_COMMON_ARC, "_common_arc"),                #        =>
        sc_type.VAR_COMMON_ARC,                                 #        || 
                                                                #        \/
        (sc_type.VAR_NODE, "_user_passing_test_history"),       # user_passing_test_history
        sc_type.VAR_PERM_POS_ARC,                               #                <-
        ScKeynodes.resolve("nrel_user_passing_test_history", sc_type.CONST_NODE_NON_ROLE)
    )
    templ.triple(
        user,
        "_common_arc", # => 
        test
    )
    search_results = search_by_template(templ)
        
    if search_results:
        search_result = search_results[0]
        return search_result.get("_user_passing_test_history")
    
    return ScAddr()

async def get_current_test(user: ScAddr) -> ScAddr:
    templ = ScTemplate()
    templ.quintuple(
        user,
        sc_type.VAR_COMMON_ARC,
        (sc_type.VAR_NODE, "test"),
        sc_type.VAR_PERM_POS_ARC,
        ScKeynodes.resolve("nrel_current_test", sc_type.VAR_NODE_NON_ROLE)
    )
    if search_results := search_by_template(templ):
        return search_results[0].get("test")
    return ScAddr()


def get_user_by_action(action: ScAddr):
    "return user and user id"
    templ = ScTemplate()
    templ.quintuple(
        action,
        sc_type.VAR_PERM_POS_ARC,
        (sc_type.VAR_NODE, "user"),
        sc_type.VAR_PERM_POS_ARC,
        ScKeynodes.rrel_index(1)
    )
    templ.quintuple(
        "user",
        sc_type.VAR_COMMON_ARC,
        (sc_type.VAR_NODE_LINK, "user_id"),
        sc_type.VAR_PERM_POS_ARC,
        ScKeynodes.resolve("nrel_tg_id", sc_type.VAR_NODE_NON_ROLE)
    )
    search_result = search_by_template(templ)[0]
    user = search_result.get("user")
    user_id = int(get_link_content_data(search_result.get("user_id")))
    return user, user_id
