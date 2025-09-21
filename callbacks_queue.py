from queue import Queue
import asyncio

from create_bot import bot

from dataclasses import dataclass
from aiogram.types import ReplyMarkupUnion

message_queue = Queue()


@dataclass
class QueueCallback:
    user_id: int | str
    text: str
    markup: ReplyMarkupUnion = None
    parse_mode: str = "markdown"


def add_to_queue(callback: QueueCallback):
    if isinstance(callback, QueueCallback):
        message_queue.put(callback)


def get_from_queue():
    try:
        return message_queue.get_nowait()
    except:
        return None


async def queue_worker():
    while True:
        task = get_from_queue()
        if task:
            await bot.send_message(chat_id=task.user_id, text=task.text, reply_markup=task.markup)
        await asyncio.sleep(1)
