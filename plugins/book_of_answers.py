import random

from nonebot import on_command
from nonebot.adapters.cqhttp import Bot, MessageEvent

from utils.data import book_of_answers

__plugin_info__ = {
    "name": "答案之书",
    "usage": {
        "答案之书": "返回一条随机的答案之书内容",
    },
    "author": "风屿",
    "version": "1.4.0",
    "permission": 2,
}

boa = on_command("答案之书", aliases={"答案之书", "答案书"}, priority=20)


@boa.handle()
async def _(bot: Bot, event: MessageEvent):
    await boa.finish(random.choice(book_of_answers))
