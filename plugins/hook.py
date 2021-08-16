"""
Author: FYWindIsland
Date: 2021-08-02 19:19:38
LastEditTime: 2021-08-15 13:02:47
LastEditors: FYWindIsland
Description: PreProcessors before matchers
I'm writing SHIT codes
"""
from typing import Dict
from nonebot import logger
from nonebot.exception import IgnoredException
from nonebot.message import run_preprocessor
from nonebot.typing import T_State
from nonebot.matcher import Matcher
from nonebot.plugin import get_plugin, get_loaded_plugins
from nonebot.adapters import Bot
from nonebot.adapters.cqhttp.event import (
    Event,
    MessageEvent,
    GroupMessageEvent,
    PrivateMessageEvent,
)

from utils.msg_util import at
from service.db.utils.perm import set_perm
from service.db.utils.ban import ban, isbanned
from service.db.utils.plugin_manager import query_plugin_status, set_plugin_status
from utils.utils import perm_check, enable_check, ExploitCheck
from configs.config import (
    OWNER,
    SUPERUSERS,
    HIDDEN_PLUGINS,
    BAN_TIME,
    BAN_CHEKC_FREQ,
    BAN_CHECK_PERIOD,
)

__permission__ = 0


@run_preprocessor  # type: ignore
async def handle_plugin_permission(
    matcher: Matcher, bot: Bot, event: Event, state: T_State
):
    if not isinstance(event, MessageEvent):
        return
    conv = {
        "user": [event.user_id],
        "group": [event.group_id] if isinstance(event, GroupMessageEvent) else [],
    }
    module_name = str(matcher.plugin_name)
    if module_name in HIDDEN_PLUGINS:
        return

    # if str(conv["user"][0]) in SUPERUSERS:
    #     return
    await __update_plugin(conv)
    if isinstance(event, MessageEvent):
        await __update_perm(event.user_id, event.sender.role)  # type: ignore
    try:
        plugin_perm = get_plugin(module_name).module.__getattribute__("__permission__")  # type: ignore
    except:
        plugin_perm = 5
    enabled = await enable_check(plugin=module_name, event=event)
    has_perm = await perm_check(perm=plugin_perm, event=event)
    if not (enabled and has_perm):
        raise IgnoredException("插件未启用或没有足够权限")


async def __update_plugin(conv={"user": [], "group": []}):
    plugin_list_current: Dict[str, bool]
    plugin_list_current = {}
    if conv["group"]:
        plugin_list_stored = await query_plugin_status(
            id=str(conv["group"][0]), isGroup=True
        )
    else:
        plugin_list_stored = await query_plugin_status(
            id=str(conv["user"][0]), isGroup=False
        )
    for p in get_loaded_plugins():
        if str(p.name) not in HIDDEN_PLUGINS:
            plugin_list_current.update({str(p.name): True})
        else:
            # logger.debug("Skip hidden plugin")
            pass
    for i in list(plugin_list_stored.keys()):
        if not i in plugin_list_current.keys():
            plugin_list_stored.pop(i)
    plugin_list_current.update(plugin_list_stored)
    if conv["group"]:
        await set_plugin_status(
            id=str(conv["group"][0]), status=plugin_list_current, isGroup=True
        )
    else:
        await set_plugin_status(
            id=str(conv["user"][0]), status=plugin_list_current, isGroup=False
        )


async def __update_perm(uid: int, role: str):
    id = str(uid)
    if id in SUPERUSERS:
        await set_perm(id=id, perm=9)
    if id in OWNER:
        await set_perm(id=id, perm=10)


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
    if matcher.type == "message" and matcher.priority not in range(0, 9):
        if await isbanned(event.user_id):
            raise IgnoredException("用户正在封禁中")
        if state["_prefix"]["raw_command"]:
            if exploit.check(f'{event.user_id}{state["_prefix"]["raw_command"]}'):
                if await ban(event.user_id, 9, BAN_TIME * 60):
                    logger.info(f"USER {event.user_id} 触发了恶意触发检测")
                await bot.send_group_msg(
                    group_id=event.group_id,
                    message=at(event.user_id) + f"检测到恶意触发命令，您将被封禁 {BAN_TIME} 分钟",
                )
                raise IgnoredException("检测到恶意触发命令")
        exploit.add(f'{event.user_id}{state["_prefix"]["raw_command"]}')
