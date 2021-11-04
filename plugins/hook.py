from nonebot import logger
from nonebot.plugin import get_plugin
from nonebot.typing import T_State
from nonebot.matcher import Matcher
from nonebot.message import run_preprocessor
from nonebot.exception import IgnoredException
from nonebot.adapters.cqhttp import Bot, Event, MessageEvent, GroupMessageEvent

from utils.utils import ExploitCheck, perm_check, enable_check
from db.models.ban import Ban
from configs.config import (
    OWNER,
    BAN_TIME,
    SUPERUSERS,
    BAN_CHEKC_FREQ,
    HIDDEN_PLUGINS,
    BAN_CHECK_PERIOD,
)
from utils.msg_util import at
from db.utils.plugin_perm import PluginPerm

__permission__ = 0


@run_preprocessor  # type: ignore
async def handle_plugin_permission(
    matcher: Matcher, bot: Bot, event: Event, state: T_State
):
    user_id = getattr(event, "user_id", None)
    group_id = getattr(event, "group_id", None)
    if user_id is None or group_id is None:
        return

    # *超级用户和主人不做权限判断
    if user_id in SUPERUSERS or user_id == OWNER:
        return
    # *插件控制系统 关闭状态>=用户权限>=群组权限
    module_name = str(matcher.module_name)
    if module_name in HIDDEN_PLUGINS:
        return
    plugin = get_plugin(module_name)
    if plugin:
        plugin_perm = await PluginPerm.get_plugin_perm(plugin.name)
    else:
        plugin_perm = 5
    enabled = await enable_check(plugin=module_name, event=event)
    has_perm = await perm_check(perm=plugin_perm, event=event)
    if not (enabled and has_perm):
        raise IgnoredException("插件未启用或没有足够权限")


@run_preprocessor  # type: ignore
async def handle_limit(matcher: Matcher, bot: Bot, event: MessageEvent, state: T_State):
    pass


exploit = ExploitCheck(BAN_CHECK_PERIOD, BAN_CHEKC_FREQ)


@run_preprocessor  # type: ignore
async def ban_exploit_check(
    matcher: Matcher, bot: Bot, event: GroupMessageEvent, state: T_State
):
    if not isinstance(event, GroupMessageEvent):
        return
    if (
        matcher.type == "message"
        and (
            matcher.priority not in range(0, 11)
            or matcher.priority not in range(90, 101)
        )
        and matcher.module_name not in HIDDEN_PLUGINS
    ):
        if await Ban.isbanned(event.user_id):
            raise IgnoredException("用户正在封禁中")
        if state["_prefix"]["raw_command"]:
            if exploit.check(f'{event.user_id}{state["_prefix"]["raw_command"]}'):
                if await Ban.ban(event.user_id, 9, BAN_TIME * 60):
                    logger.info(f"USER {event.user_id} 触发了恶意触发检测")
                await bot.send_group_msg(
                    group_id=event.group_id,
                    message=at(event.user_id) + f"检测到恶意触发命令，您将被封禁 {BAN_TIME} 分钟",
                )
                raise IgnoredException("检测到恶意触发命令")
        exploit.add(f'{event.user_id}{state["_prefix"]["raw_command"]}')
