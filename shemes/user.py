from dataclasses import dataclass
from enum import Enum

from typing import List


class ContentType(Enum):
    VIDEO = 0
    AUDIO = 1
    TEXT = 2
    VISUALIZATION = 3

class Achievement:
    ...

@dataclass
class Rating:
    knowledge_level: str
    worth_studied_themes: List[str]
    well_studied_themes: List[str]

@dataclass
class User:
    id: int
    name: str
    user_class: int
    achievements: List[Achievement]
    self_rating: Rating
    system_rating: Rating

    def __str__(self):
        return f"*{self.name}*\n" \
                f"ID: {self.id}\n" \
                f"Класс: {self.user_class}\n" \
                f"Получено достижений: {len(self.achievements)}\n\n" \
                f"Уровень знаний: {self.system_rating.knowledge_level}\n" \
                f"Самооценка: {self.self_rating.knowledge_level}"
