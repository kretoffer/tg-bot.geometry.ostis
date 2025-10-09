from dataclasses import dataclass, field
from typing import List

from sc_client.models import ScAddr, ScTemplate
from sc_client.constants import sc_type
from sc_client.client import search_by_template

from sc_kpm.sc_keynodes import ScKeynodes
from sc_kpm.utils import get_link_content_data


@dataclass
class Lesson:
    type: str
    description: str
    peculiarities: List[str] = field(default_factory=list)


    def __str__(self):
        text = self.type
        if self.peculiarities:
            text += "\n*Особенности:*\n"
            for el in self.peculiarities:
                text+=" - "+ el + "\n"
        return text
    
    
    @property
    def name(self):
        return self.type


    @classmethod
    def sc_to_lesson(cls, addr: ScAddr):
        templ = ScTemplate()
        templ.quintuple(
            addr,
            sc_type.VAR_COMMON_ARC,
            (sc_type.VAR_NODE_LINK, "_description"),
            sc_type.VAR_PERM_POS_ARC,
            ScKeynodes.resolve("nrel_description", sc_type.CONST_NODE_NON_ROLE)
        )
        if search_results := search_by_template(templ):
            description = get_link_content_data(search_results[0].get("_description"))
        else:
            description = ""
        templ = ScTemplate()
        templ.triple(
            (sc_type.VAR_NODE_CLASS, "_type"),
            sc_type.VAR_PERM_POS_ARC,
            addr
        )
        templ.triple(
            ScKeynodes.resolve("concept_content_type", sc_type.VAR_NODE_CLASS),
            sc_type.VAR_PERM_POS_ARC,
            "_type"
        )
        templ.quintuple(
            "_type",
            sc_type.VAR_COMMON_ARC,
            (sc_type.VAR_NODE_LINK, "_name"),
            sc_type.VAR_PERM_POS_ARC,
            ScKeynodes.resolve("nrel_main_idtf", sc_type.CONST_NODE_NON_ROLE)
        )
        if search_results := search_by_template(templ):
            return Lesson(
                get_link_content_data(search_results[0].get("_name")),
                description
            )
        return Lesson("Урок", description)

