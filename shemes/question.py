from dataclasses import dataclass
from typing import List, Tuple

from sc_client.models import ScAddr


@dataclass
class Question:
    text: str
    answers: List[Tuple[ScAddr, str]]
