"""
Author: FYWindIsland
Date: 2021-08-14 15:48:24
LastEditTime: 2021-08-17 21:34:08
LastEditors: FYWindIsland
Description: 
I'm writing SHIT codes
"""
from nonebot.adapters.cqhttp import Bot, MessageEvent
from nonebot.typing import T_State
from nonebot.plugin import on_command

from utils.msg_util import reply, text
from .data_source import get_sx

hhsh = on_command("好好说话", priority=5, block=False)


@hhsh.handle()
async def handle_receive(bot: Bot, event: MessageEvent, state: T_State):
    content = str(event.get_message()).strip()
    sx = await get_sx(content)
    await hhsh.finish(reply(event.user_id) + text(sx))


__usage__ = """好好说话 [缩写内容]
"""

__plugin_name__ = "缩写查询"

__permission__ = 2
