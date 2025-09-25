from sc_client.models import ScAddr, ScTemplate
from sc_client.constants import sc_type
from sc_client.client import search_by_template

from sc_kpm.utils import search_element_by_non_role_relation, search_connector, get_link_content_data
from sc_kpm import ScKeynodes


def get_ru_main_identifier(entity_addr: ScAddr) -> ScAddr:
    return search_lang_value_by_nrel_identifier(entity_addr, "nrel_main_idtf", "lang_ru")


def get_name_str(addr: ScAddr) -> ScAddr:
    return get_link_content_data(search_lang_value_by_nrel_identifier(addr, "nrel_name"))
def get_description_str(addr: ScAddr) -> ScAddr:
    return get_link_content_data(search_lang_value_by_nrel_identifier(addr, "nrel_description"))
def get_condition_str(addr: ScAddr) -> ScAddr:
    return get_link_content_data(search_lang_value_by_nrel_identifier(addr, "nrel_condition"))

    
def search_lang_value_by_nrel_identifier(entity_addr: ScAddr, idtf_str: str = "nrel_main_idtf", lang_str: str = "lang_ru") -> ScAddr:
    idtf = ScKeynodes.resolve(
        idtf_str, sc_type.CONST_NODE_NON_ROLE)
    lang = ScKeynodes.resolve(lang_str, sc_type.CONST_NODE_CLASS)

    template = ScTemplate()
    template.quintuple(
        entity_addr,
        sc_type.VAR_COMMON_ARC,
        sc_type.VAR_NODE_LINK,
        sc_type.VAR_PERM_POS_ARC,
        idtf,
    )
    search_results = search_by_template(template)
    if len(search_results) == 1:
        return search_results[0][2]
    for result in search_results:
        idtf = result[2]
        lang_edge = search_connector(
            lang, idtf, sc_type.VAR_PERM_POS_ARC)
        if lang_edge:
            return idtf
    return search_element_by_non_role_relation(
        src=entity_addr, nrel_node=idtf)