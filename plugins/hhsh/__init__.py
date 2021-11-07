from nonebot.plugin import on_command
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import Bot, MessageEvent

from utils.msg_util import text, reply

from .data_source import get_sx

hhsh = on_command("好好说话", priority=20, block=False)


@hhsh.handle()
async def handle_receive(bot: Bot, event: MessageEvent, state: T_State):
    content = str(event.get_message()).strip()
    sx = await get_sx(content)
    await hhsh.finish(reply(event.user_id) + text(sx))


__plugin_info__ = {
    "name": "好好说话",
    "des": "通过 能不能好好说话 API 查询某个缩写词的可能含义",
    "usage": {"好好说话 <缩写内容>": {"des": "查询某个缩写词的可能含义", "eg": "好好说话 cpdd"}},
    "author": "风屿",
    "version": "1.0.0",
    "permission": 2,
}
