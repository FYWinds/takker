from typing import Any, Optional

from nonebot.rule import to_me
from nonebot.plugin import on_command
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import GROUP, Bot, GroupMessageEvent

__plugin_info__ = {
    "name": "撤回",
    "des": "被动技能",
    "usage": {
        "撤回": "撤回BOT在本群内发的上一条消息",
        "回复BOT发送的消息 撤回": "撤回BOT发送的指定消息",
    },
    "author": "风屿",
    "version": "1.0.0",
    "permission": 0,
}


messages: dict[int, list[int]] = {}


@Bot.on_called_api  # type: ignore
async def _(
    bot: Bot,
    exception: Optional[Exception],
    api: str,
    data: dict[str, Any],
    result: Any,
):
    global messages
    if exception:
        return
    if api != "send_msg":
        return
    message_id = result["message_id"]
    if data["message_type"] == "group":
        if data["group_id"] in messages:
            messages[data["group_id"]].append(message_id)
        else:
            messages[data["group_id"]] = [message_id]
    else:
        pass


withdraw = on_command("撤回", priority=20, permission=GROUP, rule=to_me())


@withdraw.handle()
async def _wdh(bot: Bot, event: GroupMessageEvent, state: T_State):
    global messages
    if event.reply is None:
        message_id = messages[event.group_id].pop()
    else:
        message_id = event.reply.message_id
        del messages[event.group_id][message_id]
    await bot.delete_msg(message_id=message_id)
