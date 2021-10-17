import base64
import random
import asyncio
import traceback
from datetime import datetime, timedelta

from nonebot import get_bot
from nonebot.log import logger
from nonebot_plugin_apscheduler import scheduler

from utils.browser import get_browser
from service.db.models.bs import Bili_sub

from .bilireq import BiliReq
from .dynamic import Dynamic

DB = Bili_sub()
last_time = {}


@scheduler.scheduled_job("interval", seconds=30, id="dynamic_sched")
async def dy_sched():
    """直播推送"""

    uids = await DB.get_dynamic_bid()
    if not uids:
        return
    try:
        bot = get_bot()
    except (KeyError, ValueError):
        return
    for uid in uids:
        asyncio.sleep(2)
        name = await DB.get_user_name(uid)

        logger.debug(f"爬取动态 {name}（{uid}）")
        br = BiliReq()
        dynamics = (await br.get_user_dynamics(uid)).get("cards", [])  # 获取最近十二条动态

        if len(dynamics) == 0:  # 没有发过动态的直接结束
            continue

        if uid not in last_time:  # 没有爬取过这位主播就把最新一条动态时间为 last_time
            dynamic = Dynamic(dynamics[0])
            last_time[uid] = dynamic.time
            continue

        for dynamic in dynamics[4::-1]:  # 从旧到新取最近5条动态
            dynamic = Dynamic(dynamic)
            if (
                dynamic.time > last_time[uid]
                and dynamic.time
                > datetime.now().timestamp() - timedelta(minutes=10).seconds
            ):
                logger.info(f"检测到新动态（{dynamic.id}）：{name}（{uid}）")
                image = None
                for _ in range(3):
                    try:
                        image = await get_dynamic_screenshot(dynamic.url)
                        break
                    except Exception as e:
                        logger.error("截图失败，以下为错误日志:")
                        logger.error(traceback(e))
                    await asyncio.sleep(0.1)
                if not image:
                    logger.error("已达到重试上限，将在下个轮询中重新尝试")
                await dynamic.format(image)

                push_list = await DB.get_dynamic_push_list(uid)
                for g in push_list["group"]:
                    await bot.call_api(
                        "send_group_msg",
                        **{"message": dynamic.message, "group_id": g},
                    )
                    asyncio.sleep(random.random())
                for u in push_list["user"]:
                    await bot.call_api(
                        "send_private_msg",
                        **{"message": dynamic.message, "user_id": u},
                    )
                    asyncio.sleep(random.random())

                last_time[uid] = dynamic.time


async def get_dynamic_screenshot(url):
    browser = await get_browser()
    page = None
    try:
        page = await browser.new_page(device_scale_factor=2)
        await page.goto(url, wait_until="networkidle", timeout=10000)
        await page.set_viewport_size({"width": 2560, "height": 1080})
        card = await page.query_selector(".card")
        assert card is not None
        clip = await card.bounding_box()
        assert clip is not None
        bar = await page.query_selector(".text-bar")
        assert bar is not None
        bar_bound = await bar.bounding_box()
        assert bar_bound is not None
        clip["height"] = bar_bound["y"] - clip["y"]
        image = await page.screenshot(clip=clip)
        await page.close()
        return base64.b64encode(image).decode()
    except Exception:
        if page:
            await page.close()
        raise
