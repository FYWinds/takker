from nonebot.plugin import on_command
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import Bot, MessageEvent

from utils.msg_util import image

from .handler import get_card

__plugin_info__ = {
    "name": "签到",
    "des": "获取当日签到图片",
    "usage": {"签到|抽签|运势|.luck": {"des": "获得当日签到图片", "eg": "签到"}},
    "author": "风屿",
    "version": "1.0.0",
    "permission": 1,
}

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
    await check.finish(image(c=img))
