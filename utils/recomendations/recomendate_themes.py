from sc_client.models import ScAddr

from typing import List


async def get_recomendate_themes(*, data: str = None, result: ScAddr = None, **kwargs) -> List[ScAddr]:
    if not result:
        result_addr = data.split(":")[3]
        result = ScAddr(result_addr)

    good_themes, bad_themes, other_themes = ... # TODO

    themes_recomendation = good_themes + other_themes + bad_themes
    return themes_recomendation
