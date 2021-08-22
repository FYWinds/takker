"""
Author: FYWindIsland
Date: 2021-08-13 16:10:47
LastEditTime: 2021-08-20 22:35:11
LastEditors: FYWindIsland
Description: 
I'm writing SHIT codes
"""
import httpx
import base64
from typing import Optional

from utils.browser import get_ua
from service.db.utils.illust import get_random_illust, remove_illust
from configs.config import PIXIV_IMAGE_URL


async def get_illust(nsfw: int, keyword: Optional[str] = "") -> dict:
    a = await get_random_illust(nsfw, keyword)
    if a == {}:
        return {}
    pid = a["pid"]
    url = "https://hibi.windis.xyz/api/pixiv/illust"
    params = {"id": pid}
    async with httpx.AsyncClient(headers=get_ua()) as client:
        resp = await client.get(url=url, params=params)
    try:
        img_url = str(resp.json()["illust"]["image_urls"]["medium"]).replace(
            "i.pximg.net", PIXIV_IMAGE_URL
        )
        orig_img_url = []
        if resp.json()["illust"]["meta_single_page"]:
            orig_img_url = [
                str(
                    resp.json()["illust"]["meta_single_page"]["original_image_url"]
                ).replace("i.pximg.net", PIXIV_IMAGE_URL)
            ]
        else:
            for i in resp.json()["illust"]["meta_pages"]:
                orig_img_url += [
                    str(i["image_urls"]["original"]).replace(
                        "i.pximg.net", PIXIV_IMAGE_URL
                    )
                ]
        a.update({"img_url": img_url})
        a.update({"orig_img_url": orig_img_url})
        a.update({"error": False})
        async with httpx.AsyncClient(headers=get_ua()) as client:
            resp = await client.get(url=img_url)
        # content = base64.b64encode(resp.content)
        a.update({"img_bytes": resp.content})
        return a
    except:
        await remove_illust(a)
        return await get_illust(nsfw, keyword)
