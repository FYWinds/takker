from nonebot.typing import T_State
from nonebot.matcher import Matcher
from nonebot.message import run_preprocessor
from nonebot.adapters import Bot, Event
from nonebot.exception import IgnoredException

from utils.utils import perm_check
from configs.config import HIDDEN_PLUGINS
from db.utils.plugin_perm import PluginPerm


@run_preprocessor
async def _permission_check(matcher: Matcher, bot: Bot, event: Event, state: T_State):
    plugin_name = matcher.plugin_name
    if not plugin_name or plugin_name in HIDDEN_PLUGINS:
        return
    plugin_perm = await PluginPerm.get_plugin_perm(plugin_name)
    if await perm_check(plugin_perm, event):
        return
    else:
        raise IgnoredException("权限不足")
