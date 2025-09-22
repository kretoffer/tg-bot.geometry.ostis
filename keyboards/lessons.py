from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from sc_client.constants import sc_type
from sc_client.models import ScAddr, ScTemplate
from sc_client.client import search_by_template

from utils.lessons import get_task_for_lesson, get_test_for_lesson, get_theme_of_lesson


def get_lesson_from_message(message: ScAddr) -> ScAddr:
    templ = ScTemplate()
    templ.triple(
        (sc_type.VAR_NODE_STRUCTURE, "lesson"),
        (sc_type.VAR_PERM_POS_ARC, "arc_to_message"),
        message
    )
    lesson = search_by_template(templ)[0].get("lesson")
    return lesson


def get_next_message(message: ScAddr, lesson: ScAddr):
    templ = ScTemplate()
    templ.triple(
        lesson,
        (sc_type.VAR_PERM_POS_ARC, "arc_to_message"),
        message
    )
    templ.quintuple(
        lesson,
        sc_type.VAR_PERM_POS_ARC,
        (sc_type.VAR_NODE_LINK, "message"),
        sc_type.VAR_COMMON_ARC,
        "arc_to_message"
    )
    if search_results := search_by_template(templ):
        return search_results[0].get("message")


def get_previous_message(message: ScAddr, lesson: ScAddr):
    templ = ScTemplate()
    templ.triple(
        lesson,
        (sc_type.VAR_PERM_POS_ARC, "arc_to_message"),
        message
    )
    templ.triple(
        lesson,
        (sc_type.VAR_PERM_POS_ARC, "arc_to_previous_message"),
        (sc_type.VAR_NODE_LINK, "message")
    )
    templ.triple(
        "arc_to_previous_message",
        sc_type.VAR_COMMON_ARC,
        "arc_to_message"
    )
    if search_results := search_by_template(templ):
        return search_results[0].get("message")


def get_lesson_message_markup(message: ScAddr):
    lesson = get_lesson_from_message(message)
    next_message = get_next_message(message, lesson)
    previous_message = get_previous_message(message, lesson) 
    keyboard = []
    if next_message:
        keyboard.append([InlineKeyboardButton(
            text="Дальше >>", 
            callback_data=f"lesson-message:{next_message}"
        )])
    else:
        keyboard.extend(_get_last_message_keyboard(message, lesson))
    if previous_message:
        keyboard.append([InlineKeyboardButton(
            text="<< Назад", 
            callback_data=f"lesson-message:{previous_message}"
        )])
    return InlineKeyboardMarkup(
        inline_keyboard=keyboard
    )

def _get_last_message_keyboard(message: ScAddr, lesson: ScAddr):
    task, test = get_task_for_lesson(lesson), get_test_for_lesson(lesson)
    theme = get_theme_of_lesson(lesson)
    return [
        [InlineKeyboardButton(text="Закончить", callback_data="finish-lesson")],
        [InlineKeyboardButton(text="Решить задачу", callback_data=f"task-start:{task.value}")],
        [InlineKeyboardButton(text="Пройти тест", callback_data=f"test-start:{test.value}")],
        [InlineKeyboardButton(text="Справочник", callback_data=f"handbook_theme:{theme.value}")]
    ]
