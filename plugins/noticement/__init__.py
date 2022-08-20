from nonebot.plugin import on_shell_command
from nonebot.typing import T_State
from nonebot.exception import IgnoredException
from nonebot.adapters.cqhttp import Bot, PrivateMessageEvent

from configs.config import OWNER, SUPERUSERS

from .parser import n_parser

__permission__ = 9

__plugin_name__ = "公告"
__plugin_usage__ = f"""
{'notice list':24s} | 列出启动后发送过的所有公告
{'notice <group> -n <通知内容>':24s} | 发送一条公告到指定群聊
group可为多个群聊，用空格隔开
公告内容暂且不支持换行
"""
__plugin_author__ = "风屿"
__plugin_version__ = "1.0.0"

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
