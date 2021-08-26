import time
import httpx
import random

from configs.config import ALAPI_TOKEN
from utils.browser import get_ua
from utils.data import fortune


async def get_acg_image():
    url = "https://v2.alapi.cn/api/acg"
    params = {"token": ALAPI_TOKEN, "format": "json"}
    async with httpx.AsyncClient(headers=get_ua()) as client:
        resp = await client.get(url=url, params=params)
    try:
        return resp.json()["data"]["url"]
    except:
        return "https://file.alapi.cn/image/comic/122514-15234207140623.jpg"


async def get_stick(user_id: int):
    time_day = time.strftime("%Y%m%d", time.localtime())
    seed = int(str(user_id) + str(time_day))
    random.seed(seed)
    result = fortune[random.randint(0, 1432)]
    if "吉" not in result["FORTUNE_SUMMARY"]:
        seed = seed + 15
        result = fortune[random.randint(0, 1432)]
    return result
