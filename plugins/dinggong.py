import os
import re
import random
from typing import List

from nonebot.plugin import on_command
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import Bot, MessageEvent

from utils.msg_util import MS
from configs.path_config import VOICE_PATH

__plugin_info__ = {
    "name": "钉宫语音包",
    "usage": {
        "傲娇|钉宫": "返回一条随机的钉宫语音",
    },
    "author": "风屿",
    "version": "1.0.0",
    "permission": 3,
}

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
    await bot.send(event, MS.record(voice, "dinggong"))
    await blame.finish(text)
