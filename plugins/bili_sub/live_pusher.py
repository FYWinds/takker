import random
import asyncio

from nonebot import get_bot
from nonebot.log import logger
from nonebot.plugin import require
from nonebot.adapters.cqhttp.message import Message, MessageSegment

from service.db.models.bs import Bili_sub

from .bilireq import BiliReq

DB = Bili_sub()

status = {}

from nonebot_plugin_apscheduler import scheduler


@scheduler.scheduled_job("interval", seconds=10, id="live_sched")
async def live_sched():
    """直播推送"""
    uids = await DB.get_live_bid()

    try:
        bot = get_bot()
    except:
        return
    if not uids:
        return
    logger.debug(f"爬取直播列表，目前开播{sum(status.values())}人，总共{len(uids)}人")
    br = BiliReq()
    res = await br.get_live_list(uids)
    if not res:
        return
    for uid, info in res.items():
        new_status = 0 if info["live_status"] == 2 else info["live_status"]
        if uid not in status:
            status[uid] = new_status
            continue
        old_status = status[uid]
        if new_status != old_status and new_status:  # 判断是否推送过
            room_id = info["short_id"] if info["short_id"] else info["room_id"]
            url = "https://live.bilibili.com/" + str(room_id)
            name = info["uname"]
            title = info["title"]
            cover = (
                info["cover_from_user"] if info["cover_from_user"] else info["keyframe"]
            )
            logger.info(f"检测到开播：{name}（{uid}）")

            live_msg = (
                f"{name} 正在直播：\n{title}\n" + MessageSegment.image(cover) + f"\n{url}"
            )
            push_list = await DB.get_live_push_list(uid)
            status[uid] = new_status
            for g in push_list["group"]:
                if (await DB.get_settings(id=g, bid=uid, isGroup=True))["at"]:
                    live_msg = MessageSegment.at("all") + live_msg
                await bot.call_api(
                    "send_group_msg",
                    **{"message": live_msg, "group_id": g},
                )
                asyncio.sleep(random.random())
            for u in push_list["user"]:
                await bot.call_api(
                    "send_private_msg",
                    **{"message": live_msg, "user_id": u},
                )
                asyncio.sleep(random.random())
