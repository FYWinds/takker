import re
import random
from difflib import SequenceMatcher

from nonebot.rule import to_me
from nonebot.plugin import on_command
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import GROUP, Bot, GroupMessageEvent

from utils.data import atri_text
from utils.msg_util import record

__permission__ = 3
__plugin_name__ = "ATRI语音包"
__plugin_usage__ = f"""
{'亚托莉|atri':24s} | 获取随机一条ATRI语音
{'亚托莉|atri <要说的话>':24s} | 根据文本相似度匹配一条ATRI语音
"""
__plugin_author__ = "风屿"
__plugin_version__ = "1.0.0"

atri = on_command(
    "atri",
    aliases={
        "亚托莉",
    },
    permission=GROUP,
    priority=20,
)


@atri.handle()
async def _h(bot: Bot, event: GroupMessageEvent, state: T_State):
    args = str(event.get_message()).strip()
    if args:
        state["words"] = args


@atri.got("words")
async def _g(bot: Bot, event: GroupMessageEvent, state: T_State):
    words = state["words"]
    if words:
        diff: dict[str, float] = {}
        for text in atri_text:
            r1 = SequenceMatcher(None, words, text["s"]).ratio()
            r2 = SequenceMatcher(None, words, text["s_f"]).ratio()
            r3 = SequenceMatcher(None, words, text["s_k"]).ratio()
            diff |= {text["o"]: r1 * r2 + r3}  # 完全瞎想的计算方式，没啥特殊的意义
        diff_sorted = dict(sorted(diff.items(), key=lambda item: item[1], reverse=True))
        voice = random.choice(
            [
                list(diff_sorted.keys())[0],
                list(diff_sorted.keys())[1],
                list(diff_sorted.keys())[2],
            ]
        )
    else:
        voice = random.choice(atri_text)["o"]
    text = re.findall("(.*).mp3", voice)[0]
    await atri.send(record(voice, "atri"))
    await atri.finish(text)
