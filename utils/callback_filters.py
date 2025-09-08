from aiogram.types import CallbackQuery
from aiogram.filters import BaseFilter

class PrefixCallbackFilter(BaseFilter):
    def __init__(self, prefix: str):
        self.prefix = prefix

    async def __call__(self, query: CallbackQuery) -> bool:
        if not query.data:
            return False
        return query.data.startswith(f"{self.prefix}:")