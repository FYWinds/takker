"""
Author: FYWindIsland
Date: 2021-08-18 10:08:18
LastEditTime: 2021-08-18 12:29:39
LastEditors: FYWindIsland
Description: 
I'm writing SHIT codes
"""
import httpx
from nonebot import on_command
from nonebot.adapters.cqhttp import Bot, Event
from nonebot.typing import T_State

from configs.config import CATAPI_TOKEN
from utils.msg_util import image

__permission__ = 2
__plugin_name__ = "随机猫猫"
__usage__ = "来点猫猫"

randomcat = on_command("来点猫猫", priority=5)


@randomcat.handle()
async def handle_receive(bot: Bot, event: Event, state: T_State):
    answer_content = await cat_query()
    if answer_content:
        await randomcat.finish(image(answer_content))
    else:
        await randomcat.finish("请求失败，请稍后重试")


async def cat_query():
    url = "https://api.thecatapi.com/v1/images/search?mime_types=gif,jpg,png"
    headers = {"x-api-key": CATAPI_TOKEN}

    async with httpx.AsyncClient() as client:
        resp = await client.get(url, headers=headers)
    resp = resp.json()
    try:
        return resp[0]["url"]
    except:
        return None
