"""
Author: FYWindIsland
Date: 2021-08-14 19:36:09
LastEditTime: 2021-08-24 11:51:16
LastEditors: FYWindIsland
Description: 
I'm writing SHIT codes
"""
import re

from nonebot.plugin import on_startswith
from nonebot.adapters.cqhttp import Bot, GroupMessageEvent
from nonebot.typing import T_State

from .handle import how_many, what_time, how_long, hif, who, handle_pers


__permission__ = 1

__plugin_name__ = "问答"

__usage__ = "问内容"

ask = on_startswith("问", priority=20)


@ask.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State):
    message = event.get_plaintext().strip()[1:]
    handled = False
    if re.findall("几|多少", message):
        handled = True
        message = await how_many(message)
    if re.findall("什么时候|啥时候", message):
        handled = True
        message = await what_time(message)
    if re.findall("多久|多长时间", message):
        handled = True
        message = await how_long(message)
    if re.findall("(.)不\1", message):
        handled = True
        message = await hif(message)

    message = await handle_pers(message)

    if re.findall("谁", message):
        handled = True
        message = await who(message, event.group_id)
    if handled:
        await ask.finish(message)
    else:
        await ask.finish()
