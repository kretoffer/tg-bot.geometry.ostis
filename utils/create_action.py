from sc_async_client.constants import sc_type
from sc_async_client.models import ScConstruction, ScAddr
from sc_async_client.client import generate_elements

from sc_async_kpm.sc_keynodes import ScKeynodes


async def create_action(action: str, *args: ScAddr):
    action_class = await ScKeynodes.resolve(action, sc_type.CONST_NODE_CLASS)
    action_initiated = await ScKeynodes.resolve("action_initiated", sc_type.CONST_NODE_CLASS)
    constr = ScConstruction()
    constr.generate_node(sc_type.CONST_NODE, "action")
    constr.generate_connector(sc_type.CONST_PERM_POS_ARC, action_class, "action")
    constr.generate_connector(sc_type.CONST_PERM_POS_ARC, await ScKeynodes.resolve("action", sc_type.CONST_NODE_CLASS), "action")

    for i, arg in enumerate(args):
        constr.generate_connector(sc_type.CONST_PERM_POS_ARC, "action", arg, f"arc_{i+1}")
        constr.generate_connector(sc_type.CONST_PERM_POS_ARC, await ScKeynodes.rrel_index(i+1), f"arc_{i+1}")

    constr.generate_connector(sc_type.CONST_PERM_POS_ARC, action_initiated, "action")
    await generate_elements(constr)
