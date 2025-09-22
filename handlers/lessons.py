from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InputMediaVideo, InputMediaPhoto

from sc_client.models import ScAddr

from keyboards.start_keyboards import start_without_test_keyboard
from keyboards.lessons import get_lesson_message_markup

from config import START_PHRASE_WITHOUT_TEST

from utils.get_user import check_user_in_sc_machine, get_user
from utils.create_action import create_action
from utils.callback_filters import PrefixCallbackFilter

from sc_kpm.utils import get_link_content_data

from handlers.personal_account import cmd_accaunt


lessons_router = Router()


@lessons_router.message(Command("lessons"))
@lessons_router.message(Command("lesson"))
@lessons_router.message(F.text.lower() in ("уроки", "урок"))
async def lessons_cmd(message: Message):
    if await check_user_in_sc_machine(message.from_user.id):
        await message.answer(START_PHRASE_WITHOUT_TEST, reply_markup=start_without_test_keyboard)

    user = get_user(message.from_user.id)
    create_action("action_form_theme_recommendations_for_user_to_study", user)


@lessons_router.callback_query(PrefixCallbackFilter("lesson-theme"))
async def select_lesson_theme(query: CallbackQuery):
    theme_addr = int(query.data.split(":")[1])
    theme = ScAddr(theme_addr)

    user = get_user(query.message.chat.id)

    create_action("action_get_lesson_on_theme", user, theme)


@lessons_router.callback_query(PrefixCallbackFilter("lesson-message"))
async def lesson_message(query: CallbackQuery, bot: Bot):
    message_addr = int(query.data.split(":")[1])
    message = ScAddr(message_addr)

    markup = get_lesson_message_markup(message)

    content = get_link_content_data(message)
    content = content.split(" && ")
    if len(content) == 1:
        [content] = content
        if content.startswith("http"):
            if content.endswith((".jpg", ".jpeg", ".png")):
                bot.send_photo(query.message.chat.id, InputMediaPhoto(media=content), reply_markup=markup)
            elif content.endswith((".mp4", ".mov", ".avi")):
                bot.send_video(query.message.chat.id, InputMediaVideo(media=content), reply_markup=markup)
            else:
                bot.send_message(query.message.chat.id, content, parse_mode="markdown", reply_markup=markup)
    else:
        media = []
        caption = None
        for el in content:
            if el.endswith((".jpg", ".jpeg", ".png")):
                media.append(InputMediaPhoto(media=el, parse_mode="markdown"))
            elif el.endswith((".mp4", ".mov", ".avi")):
                media.append(InputMediaVideo(media=el, parse_mode="markdown"))
            else:
                caption = el
        media[-1].caption = caption

        bot.send_media_group(query.message.chat.id, media, reply_markup=markup)
        query.message.delete()


@lessons_router.callback_query(F.data == "finish-lesson")
async def start_reflection(query: CallbackQuery):
    cmd_accaunt(message=query.message)
    query.message.delete()