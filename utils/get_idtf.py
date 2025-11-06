from sc_async_client.models import ScAddr, ScTemplate
from sc_async_client.constants import sc_type
from sc_async_client.client import search_by_template

from sc_async_kpm.utils import get_link_content_data
from sc_async_kpm import ScKeynodes


async def get_ru_main_identifier(entity_addr: ScAddr) -> ScAddr:
    return await search_lang_value_by_nrel_identifier(entity_addr, "nrel_main_idtf", "lang_ru")
async def get_main_identifier(entity_addr: ScAddr) -> ScAddr:
    return await search_lang_value_by_nrel_identifier(entity_addr, "nrel_main_idtf")
async def get_main_identifier_str(entity_addr: ScAddr) -> str:
    return await get_link_content_data(await get_main_identifier(entity_addr))


async def get_name_str(addr: ScAddr) -> ScAddr:
    return await get_link_content_data(await search_lang_value_by_nrel_identifier(addr, "nrel_name"))
async def get_description_str(addr: ScAddr) -> ScAddr:
    return await get_link_content_data(await search_lang_value_by_nrel_identifier(addr, "nrel_description"))
async def get_condition_str(addr: ScAddr) -> ScAddr:
    return await get_link_content_data(await search_lang_value_by_nrel_identifier(addr, "nrel_condition"))

    
async def search_lang_value_by_nrel_identifier(entity_addr: ScAddr, idtf_str: str = "nrel_main_idtf", lang_str: str = None) -> ScAddr:
    idtf = await ScKeynodes.resolve(
        idtf_str, sc_type.VAR_NODE_NON_ROLE)

    template = ScTemplate()
    template.quintuple(
        entity_addr,
        sc_type.VAR_COMMON_ARC,
        (sc_type.VAR_NODE_LINK, "target"),
        sc_type.VAR_PERM_POS_ARC,
        idtf
    )
    if lang_str:
        lang = await ScKeynodes.resolve(lang_str, sc_type.CONST_NODE_CLASS)
        template.triple(
            lang,
            sc_type.VAR_PERM_POS_ARC,
            "target"
        )
    search_results = await search_by_template(template)
    if search_results:
        return search_results[0].get("target")
    return ScAddr(0)
    