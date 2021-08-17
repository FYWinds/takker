"""
Author: FYWindIsland
Date: 2021-08-16 20:21:40
LastEditTime: 2021-08-17 21:37:46
LastEditors: FYWindIsland
Description: 
I'm writing SHIT codes
"""
import re
import time
import jieba.analyse


from nonebot.adapters.cqhttp import Bot, GroupMessageEvent, GROUP
from nonebot.typing import T_State
from nonebot.plugin import on_message

from utils.msg_util import image, text
from service.db.utils.wordcloud import get_words, log_words
from configs.config import SUPERUSERS

from .draw import draw_word_cloud

__permission__ = 1

__plugin_name__ = "群消息词云总结"

__usage__ = """本群月内/年内总结
为防止刷屏故只有群管理可以使用"""


word = on_message(permission=GROUP, priority=3, block=False)


@word.handle()
async def generator(bot: Bot, event: GroupMessageEvent, state: T_State):
    uid = event.user_id
    gid = event.group_id
    msg = event.get_plaintext()
    await write_chat_record(gid, uid, msg)
    if str(uid) in SUPERUSERS or event.sender.role in ["admin", "owner"]:
        if "本群月内总结" in msg:
            await word.finish(await generate(gid, "month"))
        elif "本群年内总结" in msg:
            await word.finish(await generate(gid, "year"))


async def write_chat_record(gid: int, uid: int, msg: str):
    msg = msg.replace("\\", "/")
    filter_words = re.findall(r"\[CQ:(.*?)\]", msg, re.S)
    for i in filter_words:
        msg = msg.replace(f"[CQ:{i}]", "")
    msg = msg.replace('"', " ")
    msg_seg = " ".join(list(jieba.analyse.extract_tags(msg)))
    if not msg == "":
        await log_words(gid, uid, msg, msg_seg)


async def generate(gid: int, type: str):
    if type == "month":
        ptime = int(time.time() - 60 * 60 * 24 * 30)
    else:
        ptime = int(time.time() - 60 * 60 * 24 * 365)
    msg_seg = await get_words(gid, ptime)
    img_path = await draw_word_cloud(gid, msg_seg)
    text_ = await generate_text(ptime, len(msg_seg))
    return text(text_) + image(abspath=img_path)


async def generate_text(ptime: int, msgs: int) -> str:
    ntime = int(time.time())
    ptime_s = time.strftime("%Y年%m月%d日", time.localtime(ptime))
    ntime_s = time.strftime("%Y年%m月%d日", time.localtime(ntime))
    text_ = f"""记录时间:
{ptime_s}
---------至---------
{ntime_s}
自有记录以来，本群一共发了{msgs}条消息
下面是本群的词云:
"""
    return text_
