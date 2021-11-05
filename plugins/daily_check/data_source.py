import time
import random
from json import JSONDecodeError

import httpx
from httpx import ReadTimeout

from utils.data import fortune, msg_of_day
from utils.browser import get_ua
from configs.config import ALAPI_TOKEN


async def get_acg_image():
    url = "https://v2.alapi.cn/api/acg"
    params = {"token": ALAPI_TOKEN, "format": "json"}
    try:
        async with httpx.AsyncClient(headers=get_ua()) as client:
            resp = await client.get(url=url, params=params)
            return resp.json()["data"]["url"]
    except (KeyError, ReadTimeout, JSONDecodeError):
        return "https://file.alapi.cn/image/comic/122514-15234207140623.jpg"


async def get_stick(user_id: int):
    time_day = time.strftime("%Y%m%d", time.localtime())
    seed = int(str(user_id) + str(time_day))
    random.seed(seed)
    result = random.choice(fortune)
    if "吉" not in result["FORTUNE_SUMMARY"]:
        seed = seed + 15
        result = random.choice(fortune)
    return result


async def get_msg(user_id: int):
    time_day = time.strftime("%Y%m%d", time.localtime())
    seed = int(str(user_id) + str(time_day))
    random.seed(seed)
    result = random.choice(msg_of_day)
    return result


async def get_greet():
    hour = int(time.strftime("%H", time.localtime()))
    if hour in range(0, 6):
        return "凌晨好"
    if hour in range(6, 12):
        return "早上好"
    if hour in range(12, 18):
        return "下午好"
    if hour in range(18, 25):
        return "晚上好"
    return ""
