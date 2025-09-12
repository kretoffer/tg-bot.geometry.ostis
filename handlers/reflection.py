from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery, Message

from aiogram.exceptions import TelegramAPIError, TelegramBadRequest, TelegramNotFound

from keyboards.reflection import select_knowledge_level_keyboard
from keyboards.start_keyboards import start_without_test_keyboard
from keyboards.themes_keyboard import get_theme_keyboard
from keyboards import get_stop_keyboard

from utils.callback_filters import PrefixCallbackFilter
from utils.get_user import check_user_in_sc_machine, get_reflection_results
from utils.themes import get_themes_list

from config import START_PHRASE_WITHOUT_TEST

reflection_router = Router()


triger_phrases = (
    "рефлексия",
    "самооценка"
)
@reflection_router.message(F.text.lower().in_(triger_phrases))
@reflection_router.callback_query(F.data == "start_reflection")
async def start_reflection(query: Message | CallbackQuery):
    # TODO удаление плохо/хорошо изученных тем в самооценке пользователя
    if await check_user_in_sc_machine(query.from_user.id):
        await query.answer("Как вы оцениваете свой уровень знаний", reply_markup=select_knowledge_level_keyboard)
    else:
        await query.answer(START_PHRASE_WITHOUT_TEST, reply_markup=start_without_test_keyboard, parse_mode="markdown")


@reflection_router.callback_query(PrefixCallbackFilter("self-kn-level"))
async def set_self_knowledge_level(query: CallbackQuery):
    # TODO Запись уровня знаний в БЗ
    themes = await get_themes_list()
    markup = get_theme_keyboard("self-worth-theme", "themes_page", themes, page=0, page_size=10, nav_postfix="self-worth-theme")
    await query.message.answer("Нажми когда выберешь все плохо изученные темы", reply_markup=get_stop_keyboard("self-worth-theme", str(query.message.message_id)))
    await query.message.edit_text("Выберите темы, которые вы плохо знаете", reply_markup=markup)


@reflection_router.callback_query(PrefixCallbackFilter("self-worth-theme"))
async def set_self_worth_theme(query: CallbackQuery):
    theme_id = int(query.data.split(":")[1])
    # TODO Запись плохо изученных тем в БЗ
    
    themes = await get_themes_list()
    theme_name = themes[theme_id]
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
    markup = get_theme_keyboard("self-well-theme", "themes_page", themes, page=0, page_size=10, nav_postfix="self-well-theme")
    message = await bot.send_message(query.message.chat.id,"Выберите темы, которые вы хорошо знаете", reply_markup=markup)
    await query.message.answer("Нажми когда выберешь все хорошо изученные темы", reply_markup=get_stop_keyboard("self-well-theme", str(message.message_id)))


@reflection_router.callback_query(PrefixCallbackFilter("self-well-theme"))
async def set_self_well_theme(query: CallbackQuery):
    theme_id = int(query.data.split(":")[1])
    # TODO Запись хорошо изученных тем в БЗ
    
    themes = await get_themes_list()
    theme_name = themes[theme_id]
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
    reflection_results = await get_reflection_results(query.from_user.id)
    await query.message.answer(f"*Результаты рефлексии:*\n\n{reflection_results}", parse_mode="markdown")