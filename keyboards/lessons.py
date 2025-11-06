from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from sc_async_client.constants import sc_type
from sc_async_client.models import ScAddr, ScTemplate
from sc_async_client.client import search_by_template

from sc_async_kpm.sc_keynodes import ScKeynodes

from utils.lessons import get_task_for_lesson, get_test_for_lesson, get_theme_of_lesson, get_firs_lesson_link


async def get_lesson_from_message(message: ScAddr) -> ScAddr:
    templ = ScTemplate()
    templ.triple(
        (sc_type.VAR_NODE_TUPLE, "_message_set"),
        (sc_type.VAR_PERM_POS_ARC, "arc_to_message"),
        message
    )
    templ.quintuple(
        (sc_type.VAR_NODE, "lesson"),
        sc_type.VAR_COMMON_ARC,
        "_message_set",
        sc_type.VAR_PERM_POS_ARC,
        await ScKeynodes.resolve("nrel_lesson_content", sc_type.VAR_NODE_NON_ROLE)
    )
    lesson = (await search_by_template(templ))[0].get("lesson")
    return lesson


async def get_next_message(message: ScAddr, lesson: ScAddr):
    templ = ScTemplate()
    templ.quintuple(
        lesson,
        sc_type.VAR_COMMON_ARC,
        (sc_type.VAR_NODE_TUPLE, "_message_set"),
        sc_type.VAR_PERM_POS_ARC,
        await ScKeynodes.resolve("nrel_lesson_content", sc_type.VAR_NODE_NON_ROLE)
    )
    templ.triple(
        "_message_set",
        (sc_type.VAR_PERM_POS_ARC, "arc_to_message"),
        message
    )
    templ.quintuple(
        "_message_set",
        sc_type.VAR_PERM_POS_ARC,
        (sc_type.VAR_NODE_LINK, "message"),
        sc_type.VAR_COMMON_ARC,
        "arc_to_message"
    )
    if search_results := await search_by_template(templ):
        return search_results[0].get("message")


async def get_previous_message(message: ScAddr, lesson: ScAddr):
    templ = ScTemplate()
    templ.quintuple(
        lesson,
        sc_type.VAR_COMMON_ARC,
        (sc_type.VAR_NODE_TUPLE, "_message_set"),
        sc_type.VAR_PERM_POS_ARC,
        await ScKeynodes.resolve("nrel_lesson_content", sc_type.VAR_NODE_NON_ROLE)
    )
    templ.triple(
        "_message_set",
        (sc_type.VAR_PERM_POS_ARC, "arc_to_message"),
        message
    )
    templ.triple(
        "_message_set",
        (sc_type.VAR_PERM_POS_ARC, "arc_to_previous_message"),
        (sc_type.VAR_NODE_LINK, "message")
    )
    templ.triple(
        "arc_to_previous_message",
        sc_type.VAR_COMMON_ARC,
        "arc_to_message"
    )
    if search_results := await search_by_template(templ):
        return search_results[0].get("message")


async def get_lesson_message_markup(message: ScAddr):
    lesson = await get_lesson_from_message(message)
    next_message = await get_next_message(message, lesson)
    previous_message = await get_previous_message(message, lesson) 
    keyboard = []
    if next_message:
        keyboard.append([InlineKeyboardButton(
            text="Дальше >>", 
            callback_data=f"lesson-message:{next_message.value}"
        )])
    else:
        keyboard.extend(await _get_last_message_keyboard(message, lesson))
    if previous_message:
        keyboard.append([InlineKeyboardButton(
            text="<< Назад", 
            callback_data=f"lesson-message:{previous_message.value}"
        )])
    return InlineKeyboardMarkup(
        inline_keyboard=keyboard
    )

async def _get_last_message_keyboard(message: ScAddr, lesson: ScAddr):
    task, test = await get_task_for_lesson(lesson), await get_test_for_lesson(lesson)
    theme = await get_theme_of_lesson(lesson)
    return [
        [InlineKeyboardButton(text="Закончить", callback_data="finish-lesson")],
        #[InlineKeyboardButton(text="Решить задачу", callback_data=f"task-start:{task.value}")],
        [InlineKeyboardButton(text="Пройти тест", callback_data=f"test-start:{test.value}")],
        #[InlineKeyboardButton(text="Справочник", callback_data=f"handbook_theme:{theme.value}")]
    ]


async def get_markup_for_start_lesson(lesson: ScAddr):
    message = await get_firs_lesson_link(lesson)
    message_addr = message.value
    return InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="Начать урок", callback_data=f"lesson-message:{message_addr}")]]
    )
