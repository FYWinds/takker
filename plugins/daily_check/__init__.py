"""
Author: FYWindIsland
Date: 2021-08-12 09:36:04
LastEditTime: 2021-08-23 17:45:26
LastEditors: FYWindIsland
Description: 
I'm writing SHIT codes
"""
from nonebot.adapters.cqhttp import (
    Bot,
    MessageEvent,
)
from nonebot.plugin import on_command
from nonebot.typing import T_State

from utils.msg_util import image
from configs.config import SUPERUSERS

from .handler import get_card

__permission__ = 1

__plugin_name__ = "每日签到"

__usage__ = "签到"


check = on_command(
    "签到",
    aliases={
        "抽签",
        "运势",
        ".luck",
    },
    priority=20,
)


@check.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    if event.get_plaintext() != "":
        return
    user_id = event.user_id
    img = await get_card(user_id)
    await check.finish(image(img, "check_in"))
