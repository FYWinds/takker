from nonebot.plugin import on_command
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import GROUP, Bot, GroupMessageEvent

from utils.msg_util import image

from . import stat_hook
from .draw import draw_stat, draw_xp_stat

__permission__ = 1
__plugin_name__ = "插件调用统计"
__usage__ = """插件调用统计 | 返回插件的调用情况
xp统计 | 返回pix搜索关键词调用情况
"""

plugin_stat = on_command(
    "插件调用统计",
    aliases={
        "功能调用统计",
        "调用统计",
    },
    priority=20,
    permission=GROUP,
    block=False,
)


@plugin_stat.handle()
async def _psh(bot: Bot, event: GroupMessageEvent, state: T_State):
    pic_file = await draw_stat(event.group_id)
    await plugin_stat.finish(image(c=pic_file))


xp_stat = on_command("xp统计", priority=20, permission=GROUP, block=False)


@xp_stat.handle()
async def _xsh(bot: Bot, event: GroupMessageEvent, state: T_State):
    pic_file = await draw_xp_stat(event.group_id)
    await plugin_stat.finish(image(c=pic_file))
