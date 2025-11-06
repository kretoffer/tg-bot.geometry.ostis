import logging
from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from sc_async_client.client import connect
from sc_async_client.constants import sc_type
from sc_async_client.constants.common import ScEventType
from sc_async_client.models.sc_event_subscription import ScEventSubscriptionParams
from sc_async_client.client import create_elementary_event_subscriptions

from sc_async_kpm.sc_keynodes import ScKeynodes


#                   LOGGING
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("logger")


#                   SC-MACHINE
async def on_startup():
    url = "ws://localhost:8090/ws_json"
    await connect(url)
    #                   CALLBACKS
    from callbacks import action_event_callback, action_event_no_callback, init_callbacks
    await init_callbacks()
    bounded_elem_addr = await ScKeynodes.resolve("action_finished_successfully", sc_type.CONST_NODE_CLASS)
    bounded_elem_no_addr = await ScKeynodes.resolve("action_finished_unsuccessfully", sc_type.CONST_NODE_CLASS)
    event_type = ScEventType.AFTER_GENERATE_OUTGOING_ARC
    event_subscription_params = ScEventSubscriptionParams(bounded_elem_addr, event_type, action_event_callback)
    event_subscription_params_no = ScEventSubscriptionParams(bounded_elem_no_addr, event_type, action_event_no_callback)
    event_subscription = await create_elementary_event_subscriptions(event_subscription_params)
    event_subscription_no = await create_elementary_event_subscriptions(event_subscription_params_no)


#                   BOT
from create_bot import bot
dp = Dispatcher(storage=MemoryStorage())
dp.startup.register(on_startup)
