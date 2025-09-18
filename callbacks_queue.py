from queue import Queue
import asyncio

from create_bot import bot

message_queue = Queue()

def add_to_queue(user_id, text):
    message_queue.put((user_id, text))


def get_from_queue():
    try:
        return message_queue.get_nowait()
    except:
        return None


async def queue_worker():
    while True:
        task = get_from_queue()
        if task:
            user_id, text = task
            await bot.send_message(chat_id=user_id, text=text)
        await asyncio.sleep(1)
