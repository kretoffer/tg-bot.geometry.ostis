from sc_client.models import ScAddr

from utils.get_user import get_user_by_action, get_reflection_results

from callbacks_queue import add_to_queue, QueueCallback


async def show_progress_callback(src: ScAddr, connector: ScAddr, trg: ScAddr):
    user, user_id = get_user_by_action(trg)

    reflection_results = await get_reflection_results(trg)
    add_to_queue(QueueCallback(user_id=user_id, text=f"*Результаты рефлексии:*\n\n{reflection_results}", parse_mode="markdown"))
