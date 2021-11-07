from nonebot.plugin import on_shell_command
from nonebot.typing import T_State
from nonebot.exception import IgnoredException
from nonebot.adapters.cqhttp import Bot, MessageEvent, GroupMessageEvent

from configs.config import SUPERUSERS
from utils.img_util import textToImage
from utils.msg_util import image

from .parser import pm_parser

__permission__ = 0

__plugin_name__ = "插件管理器"
__plugin_usage__ = f"""
{'pm list':24s} | 查看当前会话插件列表
{'pm ban <plugin>':24s} | 禁用插件
{'pm unban <plugin>':24s} | 启用插件
plugin可以为多个插件，用空格分隔
"""
__plugin_author__ = "风屿"
__plugin_version__ = "1.4.0"

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
            await bot.send(event, image(c=await textToImage(message)))
