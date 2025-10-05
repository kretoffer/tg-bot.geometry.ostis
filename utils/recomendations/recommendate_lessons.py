from sc_client.models import ScAddr, ScTemplate
from sc_client.constants import sc_type
from sc_client.client import search_by_template

from sc_kpm.sc_keynodes import ScKeynodes
from sc_kpm.sc_sets import ScSet

from typing import List


async def get_recommendated_lessons(*, data: str = None, result: ScAddr = None, **kwargs) -> List[ScAddr]:
    if not result:
        result_addr = int(data.split(":")[3])
        result = ScAddr(result_addr)

    templ = ScTemplate()
    templ.triple(
        result,
        sc_type.VAR_PERM_POS_ARC,
        (sc_type.VAR_NODE, "_result")
    )
    templ.triple(
        "_result",
        sc_type.VAR_PERM_POS_ARC,
        (sc_type.VAR_NODE, "_lesson")
    )
    search_results = search_by_template(templ)
    lessons = [search_result.get("_lesson") for search_result in search_results]
    return lessons
