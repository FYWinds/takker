import re
import random
from difflib import ndiff
from nonebot.rule import to_me
from nonebot.plugin import on_command
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import GROUP, Bot, GroupMessageEvent

from utils.data import atri_text
from utils.msg_util import record

__plugin_info__ = {
    "name": "ATRI语音包",
    "des": "从游戏ATRI My Dear Moments内提取出来的ATRI原味语音！",
    "usage": {
        "亚托莉|atri": "获取随机一条ATRI语音",
        "亚托莉|atri <要说的话>": {"des": "根据文本相似度匹配一条ATRI语音", "eg": "亚托莉|atri 晚安"},
    },
    "author": "风屿",
    "version": "1.0.0",
    "permission": 3,
}


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
    if args := str(event.get_message()).strip():
        state["words"] = args


@atri.got("words")
async def _g(bot: Bot, event: GroupMessageEvent, state: T_State):
    if words := state["words"]:
        diff: dict[str, float] = {}
        for text in atri_text:
            s_similarity = 1 - (
                len(list(ndiff(words, text["s"])))
                - sum(i[0] == " " for i in ndiff(words, text["s"]))
            ) / max(len(words), len(text["s"]))
            s_f_similarity = 1 - (
                len(list(ndiff(words, text["s_f"])))
                - sum(i[0] == " " for i in ndiff(words, text["s_f"]))
            ) / max(len(words), len(text["s_f"]))
            s_k_similarity = 1 - (
                len(list(ndiff(words, text["s_k"])))
                - sum(i[0] == " " for i in ndiff(words, text["s_k"]))
            ) / max(len(words), len(text["s_k"]))
            diff |= {text["o"]: s_similarity * 0.5 + s_f_similarity * 0.3 + s_k_similarity * 0.2}
        diff_sorted = dict(sorted(diff.items(), key=lambda item: item[1], reverse=True))
        voice = random.choice(list(diff_sorted.keys())[:3])
    else:
        voice = random.choice(atri_text)["o"]
    text = re.findall("(.*).mp3", voice)[0]
    await atri.send(record(voice, "atri"))
    await atri.finish(text)
