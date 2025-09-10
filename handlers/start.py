from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from sc_client.constants import sc_type
from sc_client.models import ScTemplate, ScLinkContent, ScLinkContentType, ScConstruction
from sc_client.client import search_by_template, create_elements

from sc_kpm import ScKeynodes

from keyboards.start_keyboards import start_keyboard, start_without_test_keyboard

from utils.get_rating import get_system_rating


start_router = Router()

async def check_user_in_sc_machine(user_id: int) -> bool:
    constr = ScConstruction()
    constr.generate_link(sc_type.CONST_NODE_LINK, ScLinkContent(user_id, ScLinkContentType.INT))
    link_user_id = create_elements(constr)[0]
    templ = ScTemplate()
    templ.quintuple(
        (sc_type.VAR_NODE, "user"),
        sc_type.VAR_COMMON_ARC,
        link_user_id,
        sc_type.VAR_PERM_POS_ARC,
        ScKeynodes.resolve("nrel_tg_id", sc_type.NODE_NON_ROLE)
    )
    if search_results := search_by_template(templ):
        user = search_results[0].get("user")
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
            sc_type.VAR_PERM_POS_ARC,
            ScKeynodes("rrel_knowledge_level", sc_type.CONST_NODE_ROLE)
        )
        if search_by_template(templ):
            return True
    return False

@start_router.message(CommandStart())
async def cmd_start(message: Message):
    user_id = message.from_user.id
    if await check_user_in_sc_machine(user_id):
        await message.answer("Что вы хотите сделать?",
                             reply_markup=start_keyboard)
    else:
        await message.answer("*Вы пока что не прошли тест*\n" \
        "Вы можете:\n - Пройти тест для разблокировки всех функций \n - Воспользоваться справочником",
        parse_mode="markdown",
        reply_markup=start_without_test_keyboard)
