from typing import Any, Optional

from nonebot.plugin import on_command
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import GROUP, Bot, GroupMessageEvent

from utils.rule import admin

__permission__ = 0
__plugin_name__ = "撤回"
__usage__ = "撤回回复的消息"

messages: list[int] = []


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
    messages.append(message_id)


withdraw = on_command("撤回", priority=20, permission=GROUP, rule=admin())


@withdraw.handle()
async def _wdh(bot: Bot, event: GroupMessageEvent, state: T_State):
    global messages
    if event.reply is None:
        return
    message_id = event.reply.message_id
    if message_id in messages:
        await bot.delete_msg(message_id=message_id)
        messages.remove(message_id)
        # await bot.send(event, message="撤回成功")
