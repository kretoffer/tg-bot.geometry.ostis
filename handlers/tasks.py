from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from keyboards.start_keyboards import start_without_test_keyboard

from config import START_PHRASE_WITHOUT_TEST

from utils.get_user import check_user_in_sc_machine, get_user
from utils.create_action import create_action
from utils.callback_filters import PrefixCallbackFilter

from sc_client.models import ScAddr
from sc_client.constants import sc_type

from sc_kpm.sc_keynodes import ScKeynodes


tasks_router = Router()


class Form(StatesGroup):
    awaiting_task_answer = State()


@tasks_router.message(Command("tasks"))
@tasks_router.message(Command("task"))
@tasks_router.message(lambda msg: msg.text.lower() in ("задачи", "задача"))
async def tasks_cmd(message: Message):
    if await check_user_in_sc_machine(message.from_user.id):
        await message.answer(START_PHRASE_WITHOUT_TEST, reply_markup=start_without_test_keyboard)

    user = get_user(message.from_user.id)
    create_action(
        "action_form_theme_recommendations_for_user_to_solve_test_or_task",
        user,
        ScKeynodes.resolve("task_recommendations", sc_type.VAR_NODE)
    )


@tasks_router.callback_query(PrefixCallbackFilter("task-theme"))
async def select_lesson_theme(query: CallbackQuery):
    theme_addr = int(query.data.split(":")[1])
    theme = ScAddr(theme_addr)

    user = get_user(query.message.chat.id)

    create_action("action_form_task_recommendations_for_user", user, theme)


@tasks_router.callback_query(PrefixCallbackFilter("answer2task"))
async def answer_to_task(query: CallbackQuery, state: FSMContext):
    task_addr = int(query.data.split(":")[1])

    await state.update_data(task_addr=task_addr)
    await state.set_state(Form.awaiting_task_answer)


@tasks_router.message(Form.awaiting_task_answer)
async def handle_first(message: Message, state: FSMContext):
    data = await state.get_data()
    task_addr = data["task_addr"]
    task = ScAddr(task_addr)

    await state.clear()

    # TODO проверка ответа


@tasks_router.callback_query(PrefixCallbackFilter("clue2task"))
async def clue_to_task(query: CallbackQuery):
    task_addr = int(query.data.split(":")[1])
    task = ScAddr(task_addr)
    # TODO


@tasks_router.callback_query(PrefixCallbackFilter("send-solve2task"))
async def send_solve_to_task(query: CallbackQuery):
    task_addr = int(query.data.split(":")[1])
    task = ScAddr(task_addr)
    # TODO
