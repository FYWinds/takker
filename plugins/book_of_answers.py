import random

from nonebot import on_command
from nonebot.adapters.cqhttp import Bot, MessageEvent

from utils.data import book_of_answers

__permission__ = 2
__plugin_name__ = "答案之书"
__usage__ = "答案之书"

boa = on_command("答案之书", aliases={"答案", "答案之书", "答案书"}, priority=20)


@boa.handle()
async def _(bot: Bot, event: MessageEvent):
    await boa.finish(random.choice(book_of_answers))
