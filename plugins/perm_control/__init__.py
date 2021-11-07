from nonebot.plugin import on_shell_command
from nonebot.typing import T_State
from nonebot.exception import IgnoredException
from nonebot.adapters.cqhttp import Bot, MessageEvent, GroupMessageEvent

from configs.config import SUPERUSERS
from utils.img_util import textToImage
from utils.msg_util import image

from .parser import perm_parser

__permission__ = 0

__plugin_name__ = "权限控制"
__plugin_usage__ = f"""
{'perm get':24s} | 获取当前会话的权限
{'perm set <perm>':24s} | 设置当前会话的权限
进阶用法请查看文档
"""
__plugin_author__ = "风屿"
__plugin_version__ = "1.4.0"

perm = on_shell_command("perm", parser=perm_parser, priority=1, block=True)


@perm.handle()
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
    args.is_group = isinstance(event, GroupMessageEvent)
    args.c_user = str(event.user_id)

    if hasattr(args, "handle"):
        if not args.is_admin and not args.is_superuser:
            raise IgnoredException("权限不足")
        message = await args.handle(args)
        if message:
            await bot.send(event, image(c=await textToImage(message)))
