"""
Author: FYWindIsland
Date: 2021-08-16 16:04:08
LastEditTime: 2021-08-16 21:26:36
LastEditors: FYWindIsland
Description: 
I'm writing SHIT codes
"""
import time
from tortoise.query_utils import Q

from service.db.model.models import Wordcloud


async def get_words(gid: int, after_time: int) -> list:
    q = await Wordcloud.filter(Q(gid=gid) & Q(time__gte=after_time)).values("msg_seg")
    try:
        msg_seg = []
        for i in q:
            msg_seg += [i["msg_seg"]]
        return msg_seg
    except:
        return []


async def log_words(gid: int, uid: int, msg: str, msg_seg: str):
    await Wordcloud.create(
        gid=gid, uid=uid, time=int(time.time()), msg=msg, msg_seg=msg_seg
    )


async def delete_history():
    ptime = int(time.time()) - 60 * 60 * 24 * 365
    await Wordcloud.filter(Q(time__lte=ptime)).delete()
