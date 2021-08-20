"""
Author: FYWindIsland
Date: 2021-08-20 08:47:20
LastEditTime: 2021-08-20 15:40:16
LastEditors: FYWindIsland
Description: 
I'm writing SHIT codes
"""
import time
from typing import Dict
from nonebot import logger
from nonebot.exception import IgnoredException
from nonebot.message import run_preprocessor
from nonebot.typing import T_State
from nonebot.matcher import Matcher
from nonebot.plugin import get_plugin, get_loaded_plugins
from nonebot.adapters.cqhttp import (
    Bot,
    Event,
    GroupMessageEvent,
)

from configs.config import HIDDEN_PLUGINS
from service.db.utils.statistic import query_status, set_status

stat: Dict[int, Dict[int, Dict[str, int]]]
# {gid: {day1: {plugin: times}, day2: {plugin: times}}}


@run_preprocessor  # type: ignore
async def _(matcher: Matcher, bot: Bot, event: Event, state: T_State):
    if not isinstance(event, GroupMessageEvent):
        return
    if (
        matcher.type == "message"
        and matcher.priority not in range(0, 11)
        and matcher.priority not in range(90, 101)
    ):
        time_today = str(int(time.time() / 60 / 60 / 24))
        stats = await query_status(gid=event.group_id)
        if time_today in stats.keys():
            module_name = matcher.module_name
            assert module_name is not None
            if module_name in HIDDEN_PLUGINS:
                return
            if module_name in stats[time_today].keys():
                stats[time_today][module_name] += 1
            else:
                stats[time_today].update({module_name: 1})
        else:
            module_name = matcher.module_name
            assert module_name is not None
            stats.update({time_today: {module_name: 1}})

        await set_status(gid=event.group_id, stat=stats)
