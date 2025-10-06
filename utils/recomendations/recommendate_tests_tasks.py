from sc_client.models import ScAddr, ScTemplate
from sc_client.constants import sc_type
from sc_client.client import search_by_template

from sc_kpm.sc_keynodes import ScKeynodes
from sc_kpm.sc_sets import ScSet

from typing import List, Literal


async def _get_recomendate_tests_tasks(data: str = None, result: ScAddr = None, _type: Literal["tests", "tasks"] = "tests") -> List[ScAddr]:
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
    for i in (f"other_{_type}", f"good_{_type}", f"bad_{_type}"):
        templ.quintuple(
            "struct",
            sc_type.VAR_COMMON_ARC,
            (sc_type.VAR_NODE, f"{i}_set"),
            sc_type.VAR_PERM_POS_ARC,
            ScKeynodes.resolve(f"nrel_{i}", sc_type.VAR_NODE_NON_ROLE)
        )

    search_result = search_by_template(templ)[0]
    good_tests_set = search_result.get(f"good_{_type}_set")
    other_tests_set = search_result.get(f"other_{_type}_set")
    bad_tests_set = search_result.get(f"bad_{_type}_set")

    good_tests = list(ScSet(set_node=good_tests_set).elements_set)
    other_tests = list(ScSet(set_node=other_tests_set).elements_set)
    bad_tests = list(ScSet(set_node=bad_tests_set).elements_set)

    themes_recomendation = good_tests + other_tests + bad_tests

    return themes_recomendation


async def get_recomendate_tests(*, data: str = None, result: ScAddr = None, **kwargs) -> List[ScAddr]:
    return await _get_recomendate_tests_tasks(data, result, "tests")


async def get_recomendate_tasks(*, data: str = None, result: ScAddr = None, **kwargs) -> List[ScAddr]:
    return await _get_recomendate_tests_tasks(data, result, "tasks")
