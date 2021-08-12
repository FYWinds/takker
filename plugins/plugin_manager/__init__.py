"""
Author: FYWindIsland
Date: 2021-08-03 12:55:30
LastEditTime: 2021-08-12 18:04:24
LastEditors: FYWindIsland
Description: 
I'm writing SHIT codes
"""
from nonebot.adapters.cqhttp import (
    Bot,
    GroupMessageEvent,
    MessageEvent,
    PrivateMessageEvent,
)
from nonebot.exception import IgnoredException
from nonebot.plugin import on_shell_command
from nonebot.typing import T_State

from configs.config import SUPERUSERS
from .parser import pm_parser


__permission__ = 0

pm = on_shell_command("pm", parser=pm_parser, priority=1, block=True)


@pm.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    args = state["args"]
    args.conv = {
        "user": [event.user_id] if isinstance(event, PrivateMessageEvent) else [],
        "group": [event.group_id] if isinstance(event, GroupMessageEvent) else [],
    }
    args.is_admin = (
        event.sender.role in ["admin", "owner"]
        if isinstance(event, GroupMessageEvent)
        else False
    )
    args.is_superuser = str(event.user_id) in SUPERUSERS

    if hasattr(args, "handle"):
        if event.sender.role not in ["admin", "owner"] and not args.is_superuser:
            raise IgnoredException("权限不足")
        message = await args.handle(args)
        if message:
            await bot.send(event, message)
