import random
from typing import Optional
from tortoise.query_utils import Q

from service.db.model.illust_model import Illust


async def get_random_illust(
    nsfw: Optional[int] = 0, keywords: Optional[list] = []
) -> dict:
    if keywords:
        a = Illust.filter(Q(nsfw=nsfw))
        for k in keywords:
            a = a.filter(
                Q(tags__contains=k) | Q(title__contains=k) | Q(author__contains=k)
            )
        a = await a.values()
        if a:
            num = len(a)
            return a[random.randint(0, num - 1)]
        else:
            return {}
    else:
        a = await Illust.filter(Q(nsfw=nsfw)).values()
        num = len(a)
        return a[random.randint(0, num - 1)]


async def check_illust(pid: int):
    if await Illust.filter(Q(pid=pid)).values():
        return True
    else:
        return False


async def add_illust(a: dict):
    pid = a["pid"]
    if await check_illust(pid):
        return
    await Illust.create(
        pid=pid,
        uid=a["uid"],
        nsfw=a["nsfw"],
        title=a["title"],
        author=a["author"],
        tags=a["tags"],
        url=f"https://www.pixiv.net/artworks/{pid}",
    )


async def remove_illust(a: dict):
    """
    :说明: `remove_illust`
    > 使已失效图片无法查询
    此处为了防止误删除
    所以使用了特殊的方式
    即直接把nsfw改成3

    :参数:
      * `a: dict`: 参考数据库Model
    """
    if not a:
        return
    await Illust.filter(Q(pid=a["pid"])).update(nsfw=3)
