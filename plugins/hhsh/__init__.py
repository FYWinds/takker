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


__usage__ = """好好说话 [缩写内容]
"""

__plugin_name__ = "缩写查询"

__permission__ = 2
