"""
Author: FYWindIsland
Date: 2021-08-03 12:55:30
LastEditTime: 2021-08-18 20:02:45
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

__plugin_name__ = "插件管理器"

__usage__ = """pm list | 获取当前会话的插件里列表
pm ban [插件1] <插件x> | 禁用当前会话中的这些插件
pm unban [插件1] <插件x> | 启用当前会话中的这些插件
"""

pm = on_shell_command("pm", parser=pm_parser, priority=1, block=True)


@pm.handle()
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

    if hasattr(args, "handle"):
        if not args.is_admin and not args.is_superuser:
            raise IgnoredException("权限不足")
        message = await args.handle(args)
        if message:
            await bot.send(event, message)
