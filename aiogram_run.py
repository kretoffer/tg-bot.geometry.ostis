import asyncio
from run_app import bot, dp


from handlers.start import start_router
from handlers.diagnostic_test import diagnostic_test_router
from handlers.handbook import handbook_router
from handlers.personal_account import personal_accaunt_router
from handlers.reflection import reflection_router
from handlers.themes_page import themes_page_router


async def main():
    from callbacks_queue import queue_worker
    asyncio.create_task(queue_worker())
    dp.include_router(start_router)
    dp.include_router(diagnostic_test_router)
    dp.include_router(handbook_router)
    dp.include_router(personal_accaunt_router)
    dp.include_router(reflection_router)
    dp.include_router(themes_page_router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
