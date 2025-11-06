from sc_async_client.models import ScAddr

from utils.get_user import get_user_by_action, get_reflection_results, get_system_rating, get_rating

from create_bot import bot


async def show_progress_callback(src: ScAddr, connector: ScAddr, trg: ScAddr):
    user, user_id = await get_user_by_action(trg)

    reflection_results = await get_reflection_results(trg)
    await bot.send_message(chat_id=user_id, text=f"Результаты рефлексии:\n\n{reflection_results}")


async def simplify_callback(src: ScAddr, connector: ScAddr, trg: ScAddr):
    user, user_id = await get_user_by_action(trg)
    rating_info = await get_rating(await get_system_rating(user), user)
    kn_level = rating_info.knowledge_level

    await bot.send_message(chat_id=user_id, text=f"Ваш уровень успешно понижен до {kn_level}")


async def simplify_callback_no(src: ScAddr, connector: ScAddr, trg: ScAddr):
    user, user_id = await get_user_by_action(trg)

    await bot.send_message(chat_id=user_id, text="Не возможно сильнее понизить уровень сложности")


async def harderfy_callback(src: ScAddr, connector: ScAddr, trg: ScAddr):
    user, user_id = await get_user_by_action(trg)
    rating_info = await get_rating(await get_system_rating(user), user)
    kn_level = rating_info.knowledge_level

    await bot.send_message(chat_id=user_id, text=f"Ваш уровень успешно повышен до {kn_level}")


async def harderfy_callback_no(src: ScAddr, connector: ScAddr, trg: ScAddr):
    user, user_id = await get_user_by_action(trg)

    await bot.send_message(chat_id=user_id, text="Не возможно сильнее повысить уровень сложности")
