from sc_client.constants import sc_type
from sc_client.models import ScAddr, ScTemplate
from sc_client.client import search_by_template

from sc_kpm.sc_keynodes import ScKeynodes
from sc_kpm.utils import get_link_content_data
from sc_kpm.utils.action_utils import get_action_result, get_action_arguments

from utils.get_idtf import get_name_str
from utils.recomendations import get_recomendate_themes
from utils.get_user import get_user_by_action

from keyboards.themes_keyboard import get_theme_keyboard

from callbacks_queue import add_to_queue, QueueCallback


async def generated_recomendations_for_study_callback(src: ScAddr, connector: ScAddr, trg: ScAddr):
    user, user_id = get_user_by_action(trg)

    result = get_action_result(trg)

    themes = await get_recomendate_themes(result=result)
    indexes = [theme.value for theme in themes]
    themes = [get_name_str(theme) for theme in themes]

    markup = get_theme_keyboard("lesson-theme", "themes_page", themes, indexes, page=0, page_size=10, nav_postfix=f"lesson-theme:{result.value}")
    add_to_queue(QueueCallback(user_id=user_id, text="Выберите тему для изучения", markup=markup))


async def get_lesson_callback(src: ScAddr, connector: ScAddr, trg: ScAddr):
    user, user_id = get_user_by_action(trg)

    result = get_action_result(trg)

    # TODO получение урока, отправка сообщения пользователю с первым сообщением из урока


async def generated_recomendations_for_testing_or_solve_task_callback(src: ScAddr, connector: ScAddr, trg: ScAddr):
    user, user_id = get_user_by_action(trg)

    result = get_action_result(trg)

    themes = await get_recomendate_themes(result=result)
    indexes = [theme.value for theme in themes]
    themes = [get_name_str(theme) for theme in themes]

    _type = get_name_str(get_action_arguments(trg, 2)[1])
    markup = get_theme_keyboard(f"{_type}-theme", "themes_page", themes, indexes, page=0, page_size=10, nav_postfix=f"{_type}-theme:{result.value}")
    add_to_queue(QueueCallback(user_id=user_id, text="Выберите тему", markup=markup))


async def get_test_callback(src: ScAddr, connector: ScAddr, trg: ScAddr):
    user, user_id = get_user_by_action(trg)

    result = get_action_result(trg)

    # TODO получение и начало теста


async def get_task_callback(src: ScAddr, connector: ScAddr, trg: ScAddr):
    user, user_id = get_user_by_action(trg)

    result = get_action_result(trg)

    # TODO получение и отправка задачи
