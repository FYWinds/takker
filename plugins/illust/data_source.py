from typing import Optional

import httpx

from utils.browser import get_ua
from configs.config import PIXIV_IMAGE_URL
from service.db.models.illust import Illust


async def get_illust(nsfw: int, keywords: Optional[list] = []) -> dict:
    data = await Illust.get_random_illust(nsfw, keywords)
    if data == {}:
        return {}
    pid = data["pid"]
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
        data |= {"img_url": img_url}
        data |= {"orig_img_url": orig_img_url}
        async with httpx.AsyncClient(headers=get_ua()) as client:
            resp = await client.get(url=img_url)
        data |= {"img_bytes": resp.content}
        data |= {"is_search": False}
        return data
    except (KeyError, IndexError):
        return await get_illust(nsfw, keywords)


async def get_illust_direct(pid: str) -> dict:
    url = "https://hibi.windis.xyz/api/pixiv/illust"
    params = {"id": pid}
    data: dict = {}
    async with httpx.AsyncClient(headers=get_ua()) as client:
        resp = await client.get(url=url, params=params)
    try:
        resp = resp.json()
        tags: set[str] = set()
        for t in resp["illust"]["tags"]:
            if t["translated_name"] is not None:
                tags.add(t["translated_name"])
            else:
                tags.add(t["name"])
        data |= {"tags": ",".join(list(tags))}
        data |= {
            "pid": pid,
            "title": resp["illust"]["title"],
            "author": resp["illust"]["user"]["name"],
            "uid": resp["illust"]["user"]["id"],
        }
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
        data |= {"orig_img_url": orig_img_url}
        data |= {"is_search": True}
        data |= {"nsfw": -1}
        return data
    except (KeyError, IndexError):
        raise ValueError
