from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from sc_client.constants import sc_type
from sc_client.models import ScTemplate
from sc_client.client import search_by_template

from sc_kpm import ScKeynodes

from keyboards.start_keyboards import start_keyboard, start_without_test_keyboard

from utils.get_rating import get_system_rating
from utils.get_user import get_user

from config import START_PHRASE, START_PHRASE_WITHOUT_TEST


start_router = Router()

async def check_user_in_sc_machine(user_id: int) -> bool:
    if user := get_user(user_id):
        raiting = get_system_rating(user)
        templ = ScTemplate()
        templ.quintuple(
            (sc_type.VAR_NODE, "_knowledge_level_info"),
            sc_type.VAR_ACTUAL_TEMP_POS_ARC,
            raiting,
            sc_type.VAR_PERM_POS_ARC,
            ScKeynodes("rrel_student", sc_type.CONST_NODE_ROLE)
        )
        templ.quintuple(
            "_knowledge_level_info",
            (sc_type.VAR_ACTUAL_TEMP_POS_ARC, "_arc_to_knowledge_level"),
            (sc_type.VAR_NODE, "_knowledge_level"),
            sc_type.VAR_ACTUAL_TEMP_POS_ARC,
            ScKeynodes("rrel_knowledge_level", sc_type.CONST_NODE_ROLE)
        )
        if search_by_template(templ):
            return True
    return False

@start_router.message(CommandStart())
async def cmd_start(message: Message):
    user_id = message.from_user.id
    if await check_user_in_sc_machine(user_id):
        await message.answer(START_PHRASE,
                             reply_markup=start_keyboard)
    else:
        await message.answer(START_PHRASE_WITHOUT_TEST,
        parse_mode="markdown",
        reply_markup=start_without_test_keyboard)
