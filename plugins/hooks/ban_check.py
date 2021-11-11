from nonebot.typing import T_State
from nonebot.matcher import Matcher
from nonebot.message import run_preprocessor
from nonebot.adapters import Bot, Event
from nonebot.exception import IgnoredException
from nonebot.adapters.cqhttp import GroupMessageEvent

from db.models.ban import Ban
from configs.config import HIDDEN_PLUGINS


@run_preprocessor
async def _ban_check(matcher: Matcher, bot: Bot, event: Event, state: T_State):
    if not isinstance(event, GroupMessageEvent):
        return
    if matcher.plugin_name in HIDDEN_PLUGINS:
        return
    if matcher.priority in range(0, 11) or matcher.priority in range(91, 101):
        return
    if await Ban.isbanned(event.user_id):
        raise IgnoredException("用户正在封禁中")
