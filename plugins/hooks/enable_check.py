from nonebot.typing import T_State
from nonebot.matcher import Matcher
from nonebot.message import run_preprocessor
from nonebot.adapters import Bot, Event
from nonebot.exception import IgnoredException

from utils.utils import enable_check
from configs.config import HIDDEN_PLUGINS


@run_preprocessor
async def _enable_check(matcher: Matcher, bot: Bot, event: Event, state: T_State):
    plugin_name = matcher.plugin_name
    if not plugin_name or plugin_name in HIDDEN_PLUGINS:
        return
    if await enable_check(plugin_name, event):
        return
    else:
        raise IgnoredException("插件未启用")
