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

__permission__ = 0
__plugin_name__ = "UP主订阅"
__usage__ = "见文档"
__author__ = "SK-415"

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
