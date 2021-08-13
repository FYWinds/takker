"""
Author: FYWindIsland
Date: 2021-08-13 09:23:20
LastEditTime: 2021-08-13 11:11:16
LastEditors: FYWindIsland
Description: 
I'm writing SHIT codes
"""
from nonebot.adapters.cqhttp import (
    Bot,
    MessageEvent,
    PrivateMessageEvent,
)
from nonebot.exception import IgnoredException
from nonebot.plugin import on_shell_command
from nonebot.typing import T_State

from configs.config import SUPERUSERS, OWNER
from .parser import n_parser

__permission__ = 9


n = on_shell_command("notice", parser=n_parser, priority=1, block=True)


@n.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    args = state["args"]
    args.user = str(event.user_id)
    args.owner = args.user in OWNER
    if args.user not in SUPERUSERS:
        raise IgnoredException("权限不足")
    if not isinstance(event, PrivateMessageEvent):
        await n.finish("请在私聊中使用此功能")
    if hasattr(args, "handle"):
        message = await args.handle(args)
        if message:
            await bot.send(event, message)
