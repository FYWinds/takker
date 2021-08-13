"""
Author: FYWindIsland
Date: 2021-08-12 09:36:04
LastEditTime: 2021-08-13 09:06:38
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

check = on_command(
    "签到",
    aliases={
        "抽签",
        "运势",
        "luck",
    },
    priority=10,
)


@check.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    user_id = event.user_id
    img = await get_card(user_id)
    await check.finish(image(img, "check_in"))
