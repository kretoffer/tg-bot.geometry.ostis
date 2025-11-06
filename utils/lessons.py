from sc_async_client.models import ScAddr, ScTemplate
from sc_async_client.client import search_by_template
from sc_async_client.constants import sc_type

from sc_async_kpm.sc_keynodes import ScKeynodes

async def get_task_for_lesson(lesson: ScAddr) -> ScAddr:
    templ = ScTemplate()
    templ.quintuple(
        lesson,
        sc_type.VAR_COMMON_ARC,
        (sc_type.VAR_NODE, "task"),
        sc_type.VAR_PERM_POS_ARC,
        await ScKeynodes.resolve("nrel_task", sc_type.VAR_NODE_NON_ROLE)
    )
    task = (await search_by_template(templ))[0].get("task")
    return task


async def get_test_for_lesson(lesson: ScAddr) -> ScAddr:
    templ = ScTemplate()
    templ.quintuple(
        lesson,
        sc_type.VAR_COMMON_ARC,
        (sc_type.VAR_NODE, "test"),
        sc_type.VAR_PERM_POS_ARC,
        await ScKeynodes.resolve("nrel_test", sc_type.VAR_NODE_NON_ROLE)
    )
    test = (await search_by_template(templ))[0].get("test")
    return test


async def get_theme_of_lesson(lesson: ScAddr) -> ScAddr:
    templ = ScTemplate()
    templ.triple(
        (sc_type.VAR_NODE_TUPLE, "_lessons_set"),
        sc_type.VAR_PERM_POS_ARC,
        lesson
    )
    templ.quintuple(
        (sc_type.VAR_NODE, "_theme"),
        sc_type.VAR_COMMON_ARC,
        "_lessons_set",
        sc_type.VAR_PERM_POS_ARC,
        await ScKeynodes.resolve("nrel_lessons", sc_type.VAR_NODE_NON_ROLE)
    )
    theme = (await search_by_template(templ))[0].get("_theme")
    return theme


async def get_firs_lesson_link(lesson: ScAddr) -> ScAddr:
    templ = ScTemplate()
    templ.quintuple(
        lesson,
        sc_type.VAR_COMMON_ARC,
        (sc_type.VAR_NODE_TUPLE, "_set"),
        sc_type.VAR_PERM_POS_ARC,
        await ScKeynodes.resolve("nrel_lesson_content", sc_type.VAR_NODE_NON_ROLE)
    )
    templ.quintuple(
        "_set",
        sc_type.VAR_PERM_POS_ARC,
        (sc_type.VAR_NODE_LINK, "_link"),
        sc_type.VAR_PERM_POS_ARC,
        await ScKeynodes.rrel_index(1)
    )
    return (await search_by_template(templ))[0].get("_link")
