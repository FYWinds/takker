import re
import random
from difflib import SequenceMatcher

from nonebot.adapters.cqhttp import Bot, GroupMessageEvent, GROUP, permission
from nonebot.typing import T_State
from nonebot.plugin import on_message
from nonebot.rule import to_me

from utils.msg_util import record
from utils.data import atri_text

__permission__ = 3
__plugin_name__ = "高性能萝卜子"
__usage__ = "@Bot 想说的话"

atri = on_message(rule=to_me(), permission=GROUP, priority=50)


@atri.handle()
async def _h(bot: Bot, event: GroupMessageEvent, state: T_State):
    args = str(event.get_message()).strip()
    if args:
        state["words"] = args


@atri.got("words", prompt="想对萝卜子说什么话呢?")
async def _g(bot: Bot, event: GroupMessageEvent, state: T_State):
    words = state["words"]
    diff: dict[str, float] = {}
    for text in atri_text:
        r1 = SequenceMatcher(None, words, text["s"]).ratio()
        r2 = SequenceMatcher(None, words, text["s_f"]).ratio()
        r3 = SequenceMatcher(None, words, text["s_k"]).ratio()
        diff.update({text["o"]: r1 * r2 + r3})  # 完全瞎想的计算方式，没啥特殊的意义
    diff_sorted = dict(sorted(diff.items(), key=lambda item: item[1], reverse=True))
    voice = random.choice(
        [
            list(diff_sorted.keys())[0],
            list(diff_sorted.keys())[1],
            list(diff_sorted.keys())[2],
        ]
    )
    text = re.findall("(.*).mp3", voice)[0]
    await atri.send(record(voice, "atri"))
    await atri.finish(text)
