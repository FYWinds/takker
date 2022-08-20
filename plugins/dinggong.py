import os
import re
import random
from typing import List

from nonebot.plugin import on_command
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import Bot, MessageEvent

from utils.msg_util import record
from configs.path_config import VOICE_PATH

__permission__ = 3
__plugin_name__ = "钉宫语音包"
__plugin_usage__ = f"""
{'傲娇|钉宫':24s} | 返回一条随机的钉宫语音
"""
__plugin_author__ = "风屿"
__plugin_version__ = "1.0.0"

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
