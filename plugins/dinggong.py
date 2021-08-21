"""
Author: FYWindIsland
Date: 2021-08-21 10:45:25
LastEditTime: 2021-08-21 14:59:28
LastEditors: FYWindIsland
Description: 
I'm writing SHIT codes
"""
import os
import re
import random
from typing import List

from nonebot.adapters.cqhttp import Bot, MessageEvent
from nonebot.typing import T_State
from nonebot.plugin import on_command

from utils.msg_util import record
from configs.path_config import VOICE_PATH

__permission__ = 3
__plugin_name__ = "钉宫语音包"
__usage__ = """傲娇"""

blame = on_command(
    "傲娇",
    aliases={
        "钉宫",
    },
    priority=20,
)


@blame.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    voices: List[str] = os.listdir(f"{VOICE_PATH}dinggong")
    voice = random.choice(voices)
    text = re.findall("_(.*)_", voice)[0]
    await bot.send(event, record(voice, "dinggong"))
    await blame.finish(text)
