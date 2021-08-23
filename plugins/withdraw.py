"""
Author: FYWindIsland
Date: 2021-08-23 16:56:31
LastEditTime: 2021-08-23 19:45:14
LastEditors: FYWindIsland
Description: 
I'm writing SHIT codes
"""
from configs.config import OWNER, SUPERUSERS
from typing import Optional, Dict, Any
from nonebot.plugin import on_command
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import (
    Bot,
    GroupMessageEvent,
    GROUP,
)

__permission__ = 0
__plugin_name__ = "撤回"
__usage__ = "撤回回复的消息"

messages: list[int] = []


@Bot.on_called_api  # type: ignore
async def _(
    bot: Bot,
    exception: Optional[Exception],
    api: str,
    data: Dict[str, Any],
    result: Any,
):
    global messages
    if exception:
        return
    if api != "send_msg":
        return
    message_id = result["message_id"]
    messages.append(message_id)


withdraw = on_command("撤回", priority=20, permission=GROUP)


@withdraw.handle()
async def _wdh(bot: Bot, event: GroupMessageEvent, state: T_State):
    global messages
    if (
        str(event.user_id) not in SUPERUSERS
        and str(event.user_id) != OWNER
        and event.sender.role not in ["admin", "owner"]
    ):
        return
    if event.reply == None:
        return
    message_id = event.reply.message_id
    if message_id in messages:
        await bot.delete_msg(message_id=message_id)
        messages.remove(message_id)
        # await bot.send(event, message="撤回成功")
