from sc_async_client.models import ScAddr, ScTemplate
from sc_async_client.constants import sc_type
from sc_async_client.client import search_by_template

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
    search_results = await search_by_template(templ)
    lessons = [search_result.get("_lesson") for search_result in search_results]
    return lessons
