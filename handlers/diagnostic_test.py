from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from utils.callback_filters import PrefixCallbackFilter
from utils.get_user import get_user
from utils.create_action import create_action

from sc_client.constants import sc_type
from sc_client.models import ScAddr, ScLinkContentType

from sc_kpm.sc_keynodes import ScKeynodes
from sc_kpm.utils import generate_link

from keyboards.diagnostc_test import reg_classes_keyboard, get_reg_knowledge_level_keyboard


diagnostic_test_router = Router()


@diagnostic_test_router.message(F.text.lower() == "пройти тест")
@diagnostic_test_router.message(Command("diagnostic_test"))
@diagnostic_test_router.callback_query(F.data == "diagnostic-test")
async def cmd_start_diagnostic_test(message: Message | CallbackQuery):
    user = get_user(message.chat.id if isinstance(message, Message) else message.message.chat.id)
    if user:
        create_action("action_start_diagnostic_test", user)
    else:
        if isinstance(message, Message):
            await message.answer("Выберите класс:", reply_markup=reg_classes_keyboard)
        else:
            await message.message.edit_text("Выберите класс:", reply_markup=reg_classes_keyboard)


@diagnostic_test_router.callback_query(PrefixCallbackFilter("user-reg-class"))
async def set_user_class(query: CallbackQuery):
    user_class = query.data.split(":")[1]
    await query.message.edit_text("Выберите свой уровень знаний:", reply_markup=get_reg_knowledge_level_keyboard(user_class))


@diagnostic_test_router.callback_query(PrefixCallbackFilter("user-reg-kn-level"))
async def set_user_kn_level(query: CallbackQuery):
    [_, user_class, kn_level] = query.data.split(":")

    link_user_id = generate_link(str(query.message.chat.id), ScLinkContentType.STRING, sc_type.CONST_NODE_LINK)
    user_class_link = generate_link(user_class, ScLinkContentType.STRING, sc_type.CONST_NODE_LINK)
    user_name_link = generate_link(query.message.chat.first_name, ScLinkContentType.STRING, sc_type.CONST_NODE_LINK)
    user_kn_level_link = ScKeynodes.resolve(f"{kn_level}_knowledge_level", sc_type.CONST_NODE)

    await query.message.delete()

    create_action("action_reg_user", link_user_id, user_class_link, user_name_link, user_kn_level_link)
