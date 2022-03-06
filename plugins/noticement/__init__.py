from nonebot.plugin import on_shell_command
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import Bot, PrivateMessageEvent

from configs.config import OWNER, SUPERUSERS

from .parser import n_parser

__plugin_info__ = {
    "name": "公告",
    "des": "向指定群聊通过机器人广播一条信息",
    "superuser_usage": {
        "notice list": "查看机器人运行以来发送过的所有公告",
        "notice <group> -n <通知内容>": {
            "des": "向指定群聊发送指定公告",
            "eg": "notice 123456 2324352 -n 测试公告",
        },
    },
    "author": "风屿",
    "version": "1.0.0",
    "permission": 9,
}

n = on_shell_command("notice", parser=n_parser, priority=20, block=True)


@n.handle()
async def _(bot: Bot, event: PrivateMessageEvent, state: T_State):
    args = state["args"]
    args.user = str(event.user_id)
    args.owner = args.user in OWNER
    if args.user not in SUPERUSERS and args.user not in OWNER:
        await n.finish("权限不足")
    if not isinstance(event, PrivateMessageEvent):
        await n.finish("请在私聊中使用此功能")
    if hasattr(args, "handle"):
        message = await args.handle(args)
        if message:
            await bot.send(event, message)
