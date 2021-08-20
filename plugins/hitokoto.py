"""
Author: FYWindIsland
Date: 2021-08-17 08:50:09
LastEditTime: 2021-08-20 15:03:32
LastEditors: FYWindIsland
Description: 
I'm writing SHIT codes
"""
__permission__ = 1

__plugin_name__ = "一言"

__usage__ = """使用方法
.h 类型
类型列表：
a 动画
b 文学
c 影视
d 诗词
e 哲学
f 网易云"""

import httpx

from nonebot import on_command
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import Bot, Event

hitokoto = on_command(".h", priority=20)


@hitokoto.handle()
async def handle_hitokoto_receive(bot: Bot, event: Event, state: T_State):
    args = str(event.get_message()).strip()
    state["content"] = args


@hitokoto.got("content", prompt="")
async def handle_content(bot: Bot, event: Event, state: T_State):
    content = state["content"]
    answer_content = await hitokoto_get(content)
    await hitokoto.finish(answer_content)


async def hitokoto_get(content: str):

    help_message = """使用方法
.h 类型
类型列表：
a 动画
b 文学
c 影视
d 诗词
e 哲学
f 网易云"""

    wrong_type = "对不起，您输入的类型暂不支持"

    if len(content) == 0:
        return help_message

    content = content[0]
    content_o = ord(content)

    if content_o < 97 or content_o > 102:
        return f"{wrong_type}"

    content = content.replace("c", "h")
    content = content.replace("d", "i")
    content = content.replace("e", "k")
    content = content.replace("f", "j")
    content = content.replace("b", "d")

    url = "https://international.v1.hitokoto.cn"
    params = {"c": content}
    async with httpx.AsyncClient() as client:
        resp = await client.get(url, params=params)
    resp = resp.json()

    hitokoto_answer = f"{resp['hitokoto']}\nFrom: {resp['from']}"

    return hitokoto_answer
