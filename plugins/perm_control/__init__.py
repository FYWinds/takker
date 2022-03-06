from nonebot.plugin import on_shell_command
from nonebot.typing import T_State
from nonebot.exception import IgnoredException
from nonebot.adapters.cqhttp import Bot, MessageEvent, GroupMessageEvent

from configs.config import SUPERUSERS
from utils.img_util import textToImage
from utils.msg_util import image

from .parser import perm_parser

__plugin_info__ = {
    "name": "权限控制",
    "des": "机器人底层控制插件",
    "usage": {
        "perm get": "获取当前会话的权限等级",
        "perm set <权限等级>": {"des": "设置当前会话的权限等级", "eg": "perm set 3"},
    },
    "superuser_usage": {
        "perm list -u/-g/-p": {"des": "获取所有群聊/插件的权限等级", "eg": "perm list -g"},
        "perm get -u/-g <ID>": {"des": "获取指定用户/群聊的权限等级", "eg": "perm get -u 123456789"},
        "perm <权限等级> set -u/-g <ID>": {
            "des": "设置指定用户/群聊的权限等级",
            "eg": "perm 3 set -u 123456789",
        },
        "perm <权限等级> set -p <插件名>": {
            "des": "设置指定插件的权限等级",
            "eg": "perm 3 set -p perm_control",
        },
        "perm reset -u/-g <ID>": {
            "des": "重置指定用户/群聊的权限等级",
            "eg": "perm reset -u 123456789",
        },
        "perm reset -p <插件名>": {
            "des": "重置指定插件的权限等级",
            "eg": "perm reset -p perm_control",
        },
    },
    "author": "风屿",
    "version": "1.4.0",
    "doc": "https://takker.windis.cn/plugins/perm.html",
    "permission": 0,
}

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
