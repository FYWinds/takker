"""
Author: FYWindIsland
Date: 2021-08-13 16:10:47
LastEditTime: 2021-08-23 18:00:06
LastEditors: FYWindIsland
Description: 
I'm writing SHIT codes
"""
import httpx
from typing import Optional

from utils.browser import get_ua
from service.db.utils.illust import get_random_illust, remove_illust
from configs.config import PIXIV_IMAGE_URL


async def get_illust(nsfw: int, keywords: Optional[list] = []) -> dict:
    a = await get_random_illust(nsfw, keywords)
    if a == {}:
        return {}
    pid = a["pid"]
    url = "https://hibi.windis.xyz/api/pixiv/illust"
    params = {"id": pid}
    async with httpx.AsyncClient(headers=get_ua()) as client:
        resp = await client.get(url=url, params=params)
    try:
        resp = resp.json()
        img_url = str(resp["illust"]["image_urls"]["medium"]).replace(
            "i.pximg.net", PIXIV_IMAGE_URL
        )
        orig_img_url = []
        if resp["illust"]["meta_single_page"]:
            orig_img_url = [
                str(resp["illust"]["meta_single_page"]["original_image_url"]).replace(
                    "i.pximg.net", PIXIV_IMAGE_URL
                )
            ]
        else:
            for i in resp["illust"]["meta_pages"]:
                orig_img_url += [
                    str(i["image_urls"]["original"]).replace(
                        "i.pximg.net", PIXIV_IMAGE_URL
                    )
                ]
        a.update({"img_url": img_url})
        a.update({"orig_img_url": orig_img_url})
        async with httpx.AsyncClient(headers=get_ua()) as client:
            resp = await client.get(url=img_url)
        a.update({"img_bytes": resp.content})
        a.update({"is_search": False})
        return a
    except:
        await remove_illust(a)
        return await get_illust(nsfw, keywords)


async def get_illust_direct(pid: str) -> dict:
    url = "https://hibi.windis.xyz/api/pixiv/illust"
    params = {"id": pid}
    a: dict = {}
    async with httpx.AsyncClient(headers=get_ua()) as client:
        resp = await client.get(url=url, params=params)
    try:
        resp = resp.json()
        tags: set[str] = set()
        for t in resp["illust"]["tags"]:
            if t["translated_name"] != None:
                tags.add(t["translated_name"])
            else:
                tags.add(t["name"])
        a.update({"tags": ",".join(list(tags))})
        a.update(
            {
                "pid": pid,
                "title": resp["illust"]["title"],
                "author": resp["illust"]["user"]["name"],
                "uid": resp["illust"]["user"]["id"],
            }
        )
        orig_img_url = []
        if resp["illust"]["meta_single_page"]:
            orig_img_url = [
                str(resp["illust"]["meta_single_page"]["original_image_url"]).replace(
                    "i.pximg.net", PIXIV_IMAGE_URL
                )
            ]
        else:
            for i in resp["illust"]["meta_pages"]:
                orig_img_url += [
                    str(i["image_urls"]["original"]).replace(
                        "i.pximg.net", PIXIV_IMAGE_URL
                    )
                ]
        a.update({"orig_img_url": orig_img_url})
        a.update({"is_search": True})
        a.update({"nsfw": -1})
        return a
    except:
        raise ValueError
