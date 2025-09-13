from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery, Message

from aiogram.exceptions import TelegramAPIError, TelegramBadRequest, TelegramNotFound

from sc_client.constants import sc_type
from sc_client.models import ScTemplate, ScAddr
from sc_client.client import search_by_template, delete_elements

from sc_kpm import ScKeynodes
from sc_kpm.utils import generate_connector

from keyboards.reflection import select_knowledge_level_keyboard
from keyboards.start_keyboards import start_without_test_keyboard
from keyboards.themes_keyboard import get_theme_keyboard
from keyboards import get_stop_keyboard

from utils.callback_filters import PrefixCallbackFilter
from utils.get_user import check_user_in_sc_machine, get_reflection_results
from utils.themes import get_themes_list, get_well_studied_themes_set, get_worth_studied_themes_set, delete_themes_from_set
from utils.get_user import get_user
from utils.get_rating import get_self_rating
from utils.get_idtf import get_name_str

from config import START_PHRASE_WITHOUT_TEST

reflection_router = Router()


triger_phrases = (
    "рефлексия",
    "самооценка"
)
@reflection_router.message(F.text.lower().in_(triger_phrases))
@reflection_router.callback_query(F.data == "start_reflection")
async def start_reflection(query: Message | CallbackQuery):
    message: Message = query if query is Message else query.message

    user = get_user(message.chat.id)
    rating = get_self_rating(user)
    worth_studied_themes_set = get_worth_studied_themes_set(rating, user)
    well_studied_themes_set = get_well_studied_themes_set(rating, user)
    
    delete_themes_from_set(worth_studied_themes_set, rating)
    delete_themes_from_set(well_studied_themes_set, rating)
    
    if await check_user_in_sc_machine(message.chat.id):
        await message.answer("Как вы оцениваете свой уровень знаний", reply_markup=select_knowledge_level_keyboard)
    else:
        await message.answer(START_PHRASE_WITHOUT_TEST, reply_markup=start_without_test_keyboard, parse_mode="markdown")


@reflection_router.callback_query(PrefixCallbackFilter("self-kn-level"))
async def set_self_knowledge_level(query: CallbackQuery):
    kn_level = query.data.split(":")[1]
    user = get_user(query.message.chat.id)
    rating = get_self_rating(user)

    templ = ScTemplate()
    templ.quintuple(
        ScKeynodes.resolve("nrel_user_knowledge_level", sc_type.CONST_NODE_NON_ROLE),
        sc_type.VAR_ACTUAL_TEMP_POS_ARC,
        (sc_type.VAR_NODE, "main"),
        sc_type.VAR_PERM_POS_ARC,
        rating
    )
    templ.quintuple(
        "main",
        (sc_type.VAR_ACTUAL_TEMP_POS_ARC, "arc_to_knowledge_level"),
        (sc_type.VAR_NODE, "knowledge_level"),
        sc_type.VAR_PERM_POS_ARC,
        ScKeynodes.resolve("rrel_knowledge_level", sc_type.CONST_NODE_ROLE)
    )
    templ.triple(
        rating,
        (sc_type.VAR_PERM_POS_ARC, "arc_to_knowledge_level_from_rating"),
        "knowledge_level"
    )

    search_result = search_by_template(templ)[0]
    arc_to_knowledge_level = search_result.get("arc_to_knowledge_level")
    arc_to_knowledge_level_from_rating = search_result.get("arc_to_knowledge_level_from_rating")
    main = search_result.get("main")

    delete_elements(arc_to_knowledge_level, arc_to_knowledge_level_from_rating)

    arc = generate_connector(
        sc_type.CONST_ACTUAL_TEMP_POS_ARC,
        main,
        ScKeynodes.resolve(f"{kn_level}_knowledge_level", sc_type.CONST_NODE)
    )
    generate_connector(
        sc_type.CONST_PERM_POS_ARC,
        rating,
        ScKeynodes.resolve(f"{kn_level}_knowledge_level", sc_type.CONST_NODE)
    )
    generate_connector(
        sc_type.CONST_PERM_POS_ARC,
        ScKeynodes.resolve("rrel_knowledge_level", sc_type.CONST_NODE_ROLE),
        arc
    )
    generate_connector(
        sc_type.CONST_PERM_POS_ARC,
        rating,
        arc
    )

    themes = await get_themes_list()
    themes = [get_name_str(theme) for theme in themes]
    markup = get_theme_keyboard("self-worth-theme", "themes_page", themes, page=0, page_size=10, nav_postfix="self-worth-theme")
    await query.message.answer("Нажми когда выберешь все плохо изученные темы", reply_markup=get_stop_keyboard("self-worth-theme", str(query.message.message_id)))
    await query.message.edit_text("Выберите темы, которые вы плохо знаете", reply_markup=markup)


def link_theme_to_set(set: ScAddr, rating: ScAddr, theme: ScAddr):
    arc = generate_connector(
        sc_type.CONST_PERM_POS_ARC,
        set,
        theme
    )
    generate_connector(
        sc_type.CONST_PERM_POS_ARC,
        rating,
        theme
    )
    generate_connector(
        sc_type.CONST_PERM_POS_ARC,
        rating,
        arc
    )


@reflection_router.callback_query(PrefixCallbackFilter("self-worth-theme"))
async def set_self_worth_theme(query: CallbackQuery):
    theme_id = int(query.data.split(":")[1])
    user = get_user(query.message.chat.id)
    rating = get_self_rating(user)
    themes = await get_themes_list()
    
    themes_set = get_worth_studied_themes_set(rating, user)
    link_theme_to_set(themes_set, rating, themes[theme_id])
    
    theme_name = get_name_str(themes[theme_id])
    await query.message.answer(f"Установлена плохо изученная тема: {theme_name}\n\n_Вы можете продолжить выбирать плохоизученные темы или закончить_",
                         parse_mode="markdown")
    

@reflection_router.callback_query(PrefixCallbackFilter("self-worth-theme-stop"))
async def stop_add_worth_themes(query: CallbackQuery, bot: Bot):
    messsage_id = int(query.data.split(":")[1])
    try:
        await bot.delete_message(query.message.chat.id, messsage_id)
    except (TelegramAPIError, TelegramBadRequest, TelegramNotFound):
        pass
    await query.message.delete()

    themes = await get_themes_list()
    themes = [get_name_str(theme) for theme in themes]
    markup = get_theme_keyboard("self-well-theme", "themes_page", themes, page=0, page_size=10, nav_postfix="self-well-theme")
    message = await bot.send_message(query.message.chat.id,"Выберите темы, которые вы хорошо знаете", reply_markup=markup)
    await query.message.answer("Нажми когда выберешь все хорошо изученные темы", reply_markup=get_stop_keyboard("self-well-theme", str(message.message_id)))


@reflection_router.callback_query(PrefixCallbackFilter("self-well-theme"))
async def set_self_well_theme(query: CallbackQuery):
    theme_id = int(query.data.split(":")[1])
    user = get_user(query.message.chat.id)
    rating = get_self_rating(user)
    themes = await get_themes_list()
    
    themes_set = get_well_studied_themes_set(rating, user)
    link_theme_to_set(themes_set, rating, themes[theme_id])
    
    theme_name = get_name_str(themes[theme_id])
    await query.message.answer(f"Установлена хорошо изученная тема: {theme_name}\n\n_Вы можете продолжить выбирать плохоизученные темы или закончить_",
                         parse_mode="markdown")
    

@reflection_router.callback_query(PrefixCallbackFilter("self-well-theme-stop"))
async def stop_add_worth_themes(query: CallbackQuery, bot: Bot):
    messsage_id = int(query.data.split(":")[1])
    try:
        await bot.delete_message(query.message.chat.id, messsage_id)
    except (TelegramAPIError, TelegramBadRequest, TelegramNotFound):
        pass
    await query.message.delete()
    await bot.send_message(query.message.chat.id, "Самооценка завершена, вы можете перейти в личный кабинет /accaunt")


@reflection_router.callback_query(F.data == "reflection")
async def start_reflection(query: CallbackQuery):
    reflection_results = await get_reflection_results(query.message.chat.id)
    await query.message.answer(f"*Результаты рефлексии:*\n\n{reflection_results}", parse_mode="markdown")