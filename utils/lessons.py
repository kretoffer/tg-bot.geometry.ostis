from sc_client.models import ScAddr, ScTemplate
from sc_client.client import search_by_template
from sc_client.constants import sc_type

from sc_kpm.sc_keynodes import ScKeynodes

def get_task_for_lesson(lesson: ScAddr) -> ScAddr:
    templ = ScTemplate()
    templ.quintuple(
        lesson,
        sc_type.VAR_COMMON_ARC,
        (sc_type.VAR_NODE, "task"),
        sc_type.VAR_PERM_POS_ARC,
        ScKeynodes.resolve("nrel_task", sc_type.VAR_NODE_NON_ROLE)
    )
    task = search_by_template(templ)[0].get("task")
    return task


def get_test_for_lesson(lesson: ScAddr) -> ScAddr:
    templ = ScTemplate()
    templ.quintuple(
        lesson,
        sc_type.VAR_COMMON_ARC,
        (sc_type.VAR_NODE, "test"),
        sc_type.VAR_PERM_POS_ARC,
        ScKeynodes.resolve("nrel_test", sc_type.VAR_NODE_NON_ROLE)
    )
    test = search_by_template(templ)[0].get("test")
    return test


def get_theme_of_lesson(lesson: ScAddr) -> ScAddr:
    templ = ScTemplate()
    templ.quintuple(
        (sc_type.VAR_NODE, "theme"),
        sc_type.VAR_COMMON_ARC,
        lesson,
        sc_type.VAR_PERM_POS_ARC,
        ScKeynodes.resolve("nrel_lesson", sc_type.VAR_NODE_NON_ROLE)
    )
    theme = search_by_template(templ)[0].get("theme")
    return theme