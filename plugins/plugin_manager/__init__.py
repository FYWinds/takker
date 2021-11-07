from nonebot.plugin import on_shell_command
from nonebot.typing import T_State
from nonebot.exception import IgnoredException
from nonebot.adapters.cqhttp import Bot, MessageEvent, GroupMessageEvent

from utils.rule import admin
from configs.config import SUPERUSERS
from utils.img_util import textToImage
from utils.msg_util import image

from .parser import pm_parser

__plugin_info__ = {
    "name": "插件管理器",
    "des": "机器人底层控制插件",
    "admin_usage": {
        "pm list": "查看当前会话插件列表",
        "pm ban <插件名称> [-a/-r]": {"des": "禁用指定插件", "eg": "pm ban bili_sub"},
        "pm unban <插件名称> [-a/-r]": {"des": "启用指定插件", "eg": "pm unban bili_sub"},
    },
    "superuser_usage": {
        "pm list -u/-g <ID>": {"des": "查看指定群或用户的插件列表", "eg": "pm list -u 123456789"},
        "pm ban -u/-g <ID> <插件名称> [-a/-r]": {
            "des": "禁用指定群或用户的指定插件",
            "eg": "pm ban -u 123456789 bili_sub",
        },
        "pm unban -u/-g <ID> <插件名称> [-a/-r]": {
            "des": "启用指定群或用户的指定插件",
            "eg": "pm unban -u 123456789 bili_sub",
        },
    },
    "additional_info": """
<插件名称>可为多个插件，用空格分隔
-a/-r 为可选参数
-a/--all: 禁用所有可禁用插件
-r/--reverse: 禁用除了传入插件列表以外的所有插件
""".strip(),
    "author": "风屿",
    "version": "1.4.0",
    "permission": 0,
}

pm = on_shell_command("pm", parser=pm_parser, priority=1, block=True, rule=admin())


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
