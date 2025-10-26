from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from utils.callback_filters import PrefixCallbackFilter

from sc_kpm.sc_keynodes import ScKeynodes
from sc_client.constants import sc_type

from keyboards.change_info import (
    change_info_keyboard,
    change_class_keyboard,
    change_pref_keyboard,
    change_charects_keyboard
)
from keyboards.start_keyboards import start_without_test_keyboard
from keyboards import get_stop_keyboard

from utils.get_user import get_user, check_user_in_sc_machine
from utils.user import (
    change_user_class,
    clear_charects,
    clear_prefs,
    add_charects,
    add_perfs
)

from config import START_PHRASE_WITHOUT_TEST, CHARACTERISTICS, CONTENT_TYPES

from handlers.personal_account import cmd_accaunt


change_info_router = Router()

#                           BASE
@change_info_router.message(Command("change_info"))
@change_info_router.callback_query(F.data == "change-info")
async def change_info(query: Message | CallbackQuery):
    message: Message = query if query is Message else query.message
    user_in_sc = await check_user_in_sc_machine(message.chat.id)
    if not user_in_sc:
        await message.answer(START_PHRASE_WITHOUT_TEST, reply_markup=start_without_test_keyboard)
        return
    await message.answer("Какую информацию вы хотите изменить?", reply_markup=change_info_keyboard)

#                        CHANGE CLASS
@change_info_router.callback_query(F.data == "change-class")
async def start_change_class(query: CallbackQuery):
    await query.message.answer("Выберите свой класс", reply_markup=change_class_keyboard)


@change_info_router.callback_query(PrefixCallbackFilter("change-class"))
async def change_class(query: CallbackQuery):
    user_class = query.data.split(":")[1]
    user = get_user(query.message.chat.id)
    change_user_class(user, user_class)
    await query.message.answer(f"Ваш класс успешно изменен на: {user_class}")
    await query.message.delete()
    await cmd_accaunt(query.message)

#                       CHANGE PREFS
@change_info_router.callback_query(F.data == "change-pref")
async def start_change_pref(query: CallbackQuery):
    user = get_user(query.message.chat.id)
    clear_prefs(user)
    message = await query.message.answer("Выберите желаемые типы контента", reply_markup=change_pref_keyboard)
    await query.message.answer("Когда выберете все желаемые типы, нажмите на кнопку", reply_markup=get_stop_keyboard("change-pref", str(message.message_id)))


@change_info_router.callback_query(PrefixCallbackFilter("add-pref"))
async def change_pref(query: CallbackQuery):
    _type = query.data.split(":")[1]
    user = get_user(query.message.chat.id)
    pref = ScKeynodes.resolve(f"concept_{_type}_lesson", sc_type.CONST_NODE_CLASS)
    add_perfs(user, pref)
    await query.message.answer(f"Установлено предпочтение: {CONTENT_TYPES[_type]}")


@change_info_router.callback_query(PrefixCallbackFilter("change-pref-stop"))
async def change_pref_stop(query: CallbackQuery, bot: Bot):
    message_id = query.data.split(":")[1]
    await query.message.answer("Предпочитаемые типы контента установлены")
    await bot.delete_message(query.message.chat.id, message_id)
    await query.message.delete()

#                   CHANGE CHARECTS
@change_info_router.callback_query(F.data == "change-charects")
async def start_change_pref(query: CallbackQuery):
    user = get_user(query.message.chat.id)
    clear_charects(user)
    message = await query.message.answer("Выберите ваши особенности, если таковые имеются", reply_markup=change_charects_keyboard)
    await query.message.answer("Когда выберете все особенности, нажмите на кнопку", reply_markup=get_stop_keyboard("change-charects", str(message.message_id)))


@change_info_router.callback_query(PrefixCallbackFilter("add-charects"))
async def change_pref(query: CallbackQuery):
    id = int(query.data.split(":")[1])
    user = get_user(query.message.chat.id)
    charect = ScKeynodes.resolve(CHARACTERISTICS[id][0], sc_type.CONST_NODE_CLASS)
    add_charects(user, charect)
    await query.message.answer(f"Установлена персональная особенность: {CHARACTERISTICS[id][1]}")


@change_info_router.callback_query(PrefixCallbackFilter("change-charects-stop"))
async def change_pref_stop(query: CallbackQuery, bot: Bot):
    message_id = int(query.data.split(":")[1])
    await query.message.answer("Особенности установлены")
    await bot.delete_message(query.message.chat.id, message_id)
    await query.message.delete()
