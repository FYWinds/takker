"""
Author: FYWindIsland
Date: 2021-08-22 13:06:12
LastEditTime: 2021-08-22 13:27:42
LastEditors: FYWindIsland
Description: 
I'm writing SHIT codes
"""
import httpx

from utils.browser import get_ua
from configs.config import PIXIV_IMAGE_URL


async def get_illust_link(pid: int) -> str:
    url = "https://hibi.windis.xyz/api/pixiv/illust"
    params = {"id": pid}
    async with httpx.AsyncClient(headers=get_ua()) as client:
        resp = await client.get(url=url, params=params)
    try:
        img_url = str(resp.json()["illust"]["image_urls"]["large"]).replace(
            "i.pximg.net", PIXIV_IMAGE_URL
        )
        return img_url
    except:
        return "图片已经失效或不存在"


async def get_illust_info(pid: int) -> dict:
    url = "https://hibi.windis.xyz/api/pixiv/illust"
    params = {"id": pid}
    async with httpx.AsyncClient(headers=get_ua()) as client:
        resp = await client.get(url=url, params=params)
    resp = resp.json()
    try:
        tags = ""
        for i in resp["illust"]["tags"]:
            tags += i["translated_name"]
        a = {
            "pid": pid,
            "title": resp["illust"]["title"],
            "author": resp["illust"]["user"]["name"],
            "uid": resp["illust"]["user"]["id"],
            "tags": tags,
        }
        return a
    except:
        return {}
