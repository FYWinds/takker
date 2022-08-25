from nonebot.plugin import on_shell_command
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import (
    Bot,
    MessageEvent,
    GroupMessageEvent,
    PrivateMessageEvent,
)

from utils.rule import admin
from utils.img_util import textToImage
from utils.msg_util import image

from . import live_pusher, dynamic_pusher
from .parser import bs_parser

__plugin_info__ = {
    "name": "B站UP主订阅助手",
    "des": "Bilibili UP主的动态更新/直播提醒",
    "admin_usage": {
        "bs list": "查看订阅列表",
        "bs add <uid>": {
            "des": "添加订阅",
            "eg": "bs add 12345678  # 添加uid为12345678的UP主到订阅列表",
        },
        "bs remove <uid>": {
            "des": "删除订阅",
            "eg": "bs remove 12345678  # 从订阅列表中删除uid为12345678的UP主",
        },
    },
    "author": "风屿",
    "version": "1.3.0",
    "permission": 0,
}

bs = on_shell_command("bs", parser=bs_parser, priority=20, rule=admin())


@bs.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    args = state["args"]
    args.conv = {
        "user": event.user_id,
        "group": event.group_id if isinstance(event, GroupMessageEvent) else None,
    }
    args.is_group = isinstance(event, GroupMessageEvent)
    args.is_user = isinstance(event, PrivateMessageEvent)

    if hasattr(args, "handle"):
        message = await args.handle(args)
        img = await textToImage(message, cut=100)
        await bot.send(event, image(c=img))
