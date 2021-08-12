"""
Author: FYWindIsland
Date: 2021-08-01 07:48:46
LastEditTime: 2021-08-11 17:47:10
LastEditors: FYWindIsland
Description: 
I'm writing SHIT codes
"""
from nonebot.adapters.cqhttp import (
    Bot,
    GroupMessageEvent,
    MessageEvent,
)
from nonebot.exception import IgnoredException
from nonebot.plugin import on_shell_command
from nonebot.typing import T_State

from configs.config import SUPERUSERS
from .parser import perm_parser


__permission__ = 0

perm = on_shell_command("perm", parser=perm_parser, priority=1, block=True)


@perm.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    args = state["args"]
    args.conv = {
        "user": [event.user_id],
        "group": [event.group_id] if isinstance(event, GroupMessageEvent) else [],
    }
    args.is_admin = (
        event.sender.role in ["admin", "owner"]
        if isinstance(event, GroupMessageEvent)
        else False
    )
    args.is_superuser = str(event.user_id) in SUPERUSERS
    args.is_group = isinstance(event, GroupMessageEvent)

    if hasattr(args, "handle"):
        if event.sender.role not in ["admin", "owner"] and not args.is_superuser:
            raise IgnoredException("权限不足")
        message = await args.handle(args)
        if message:
            await bot.send(event, message)
