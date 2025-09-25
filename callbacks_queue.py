from queue import Queue
import asyncio
from aiogram import Bot

from create_bot import bot

from dataclasses import dataclass
from aiogram.types import ReplyMarkupUnion

from types import FunctionType

message_queue = Queue()


@dataclass
class QueueCallback:
    user_id: int | str
    text: str = ""
    markup: ReplyMarkupUnion = None
    parse_mode: str = "markdown"
    comp: FunctionType = None

    async def run(self):
        if self.comp:
            await self.comp(bot, self)
        else:
            await send_message_comp(bot, self)


async def send_message_comp(bot: Bot, callback: QueueCallback):
    await bot.send_message(chat_id=callback.user_id, text=callback.text, reply_markup=callback.markup)


def add_to_queue(callback: QueueCallback):
    if isinstance(callback, QueueCallback):
        message_queue.put(callback)


def get_from_queue() -> QueueCallback:
    try:
        return message_queue.get_nowait()
    except:
        return None


async def queue_worker():
    while True:
        task = get_from_queue()
        if task:
            await task.run()
        await asyncio.sleep(1)
