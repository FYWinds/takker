from nonebot.plugin import on_command
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import GROUP, Bot, GroupMessageEvent

from utils.msg_util import MS

from .draw import draw_stat, draw_xp_stat

__plugin_info__ = {
    "name": "机器人统计数据",
    "des": "各功能调用相关统计",
    "usage": {
        "调用统计": "调取本群一个月内的插件调用统计",
        "xp统计": "调取本群一个月内的pix关键词搜索统计",
    },
    "author": "风屿",
    "version": "1.1.0",
    "permission": 1,
}

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
    await plugin_stat.finish(MS.image(c=pic_file))


xp_stat = on_command("xp统计", priority=20, permission=GROUP, block=False)


@xp_stat.handle()
async def _xsh(bot: Bot, event: GroupMessageEvent, state: T_State):
    pic_file = await draw_xp_stat(event.group_id)
    await plugin_stat.finish(MS.image(c=pic_file))
