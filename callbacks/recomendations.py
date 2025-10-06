from sc_client.models import ScAddr, ScTemplate
from sc_client.client import search_by_template
from sc_client.constants import sc_type

from sc_kpm.utils.action_utils import get_action_result, get_action_arguments
from sc_kpm.utils import get_link_content_data

from utils.get_idtf import get_name_str, get_condition_str, get_main_identifier
from utils.recomendations import get_recomendate_themes, get_recommendated_lessons, get_recomendate_tasks, get_recomendate_tests
from utils.get_user import get_user_by_action
from utils.create_action import create_action
from utils.send_message_with_content import send_message_with_content_comp

from keyboards.themes_keyboard import get_theme_keyboard
from keyboards.tasks import get_task_markup
from keyboards.lessons import get_markup_for_start_lesson

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
    
    lessons = await get_recommendated_lessons(result=result)
    indexes = [lesson.value for lesson in lessons]
    if len(lessons) == 1:
        [lesson] = lessons
        markup = get_markup_for_start_lesson(lesson)
        add_to_queue(QueueCallback(user_id, "Найден один урок по вашему запросу", markup=markup))
    else:
        markup = get_theme_keyboard("start-lesson", "themes_page", indexes, indexes, page=0, page_size=10, nav_postfix=f"start-lesson:{result.value}")
        add_to_queue(QueueCallback(user_id, "Найдено несколько уроков по вашему запросу", markup=markup))


async def get_lesson_no_callback(src: ScAddr, connector: ScAddr, trg: ScAddr):
    _, user_id = get_user_by_action(trg)

    add_to_queue(QueueCallback(user_id=user_id, text="К сожалению не удалось найти уроков по выбранной вами теме"))


async def generated_recomendations_for_testing_or_solve_task_callback(src: ScAddr, connector: ScAddr, trg: ScAddr):
    user, user_id = get_user_by_action(trg)

    result = get_action_result(trg)

    themes = await get_recomendate_themes(result=result)
    indexes = [theme.value for theme in themes]
    themes = [get_name_str(theme) for theme in themes]

    _type = get_link_content_data(get_main_identifier(get_action_arguments(trg, 2)[1]))
    markup = get_theme_keyboard(f"{_type}-theme", "themes_page", themes, indexes, page=0, page_size=10, nav_postfix=f"{_type}-theme:{result.value}")
    add_to_queue(QueueCallback(user_id=user_id, text="Выберите тему", markup=markup))


async def get_test_callback(src: ScAddr, connector: ScAddr, trg: ScAddr):
    user, user_id = get_user_by_action(trg)

    result = get_action_result(trg)

    tests = await get_recomendate_tests(result=result)
    indexes = [test.value for test in tests]
    if len(tests) == 1:
        [test] = tests
        create_action("action_start_test", user, test)
    else:
        markup = get_theme_keyboard("test-start", "themes_page", indexes, indexes, page=0, page_size=10, nav_postfix=f"test-start:{result.value}")
        add_to_queue(QueueCallback(user_id, "Найдено несколько тестов по вашему запросу", markup=markup))


async def get_task_callback(src: ScAddr, connector: ScAddr, trg: ScAddr):
    user, user_id = get_user_by_action(trg)

    result = get_action_result(trg)

    return # заглушка
    # TODO получение task: ScAddr
    condition = get_condition_str(task)
    markup = get_task_markup(task.value)
    add_to_queue(QueueCallback(user_id, condition, markup, comp=send_message_with_content_comp))
