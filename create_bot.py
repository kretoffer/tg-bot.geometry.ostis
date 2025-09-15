import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from decouple import config

from sc_client.client import connect
from sc_client.constants import sc_type
from sc_client.constants.common import ScEventType
from sc_client.models.sc_event_subscription import ScEventSubscriptionParams
from sc_client.client import create_elementary_event_subscriptions

from sc_kpm.sc_keynodes import ScKeynodes

from callbacks import action_event_callback


#                   LOGGING
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("logger")


#                   BOT
bot = Bot(token=config('TOKEN'), default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=MemoryStorage())


#                   SC-MACHINE
url = "ws://localhost:8090/ws_json"
connect(url)


#                   CALLBACKS
bounded_elem_addr = ScKeynodes.resolve("action_finished_successfully", sc_type.CONST_NODE_CLASS)
event_type = ScEventType.AFTER_GENERATE_OUTGOING_ARC
event_subscription_params = ScEventSubscriptionParams(bounded_elem_addr, event_type, action_event_callback)
event_subscription = create_elementary_event_subscriptions(event_subscription_params)
