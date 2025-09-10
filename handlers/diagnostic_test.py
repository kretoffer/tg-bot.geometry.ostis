from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from shemes.question import Question
from keyboards.diagnostc_test import get_question_keyboard
from keyboards import free_inline_markup
from utils.callback_filters import PrefixCallbackFilter

from random import randint

diagnostic_test_router = Router()


async def get_question() -> Question:
    "Нахождение вопроса и вариантов ответа"
    ... # при получении вопроса на который уже получен ответ return None
    return Question(f"question {randint(0, 50)}", [str(el) for el in range(0, 4)]) # Затычка


async def set_answer():
    "Запись ответа пользователя в БЗ"


@diagnostic_test_router.message(F.text == "Пройти тест")
@diagnostic_test_router.message(Command("test"))
async def cmd_start_diagnostic_test(message: Message):
    # Запуск теста TODO
    question = await get_question()
    await message.answer(question.text, parse_mode="markdown", reply_markup=get_question_keyboard(question))


@diagnostic_test_router.callback_query(PrefixCallbackFilter("test_answer"))
async def answer_to_question(query: CallbackQuery):
    await set_answer()
    question = await get_question()
    if question:
        await query.message.edit_text(text=question.text, parse_mode="markdown", reply_markup=get_question_keyboard(question))
    else:
        await query.message.edit_text(text="Тест завершен", reply_markup=free_inline_markup)


