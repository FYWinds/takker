import random
from typing import Optional

from tortoise.fields.data import IntField, TextField
from tortoise.models import Model
from tortoise.query_utils import Q


class Illust(Model):
    """图库"""

    pid = IntField(pk=True)
    uid = IntField()
    nsfw = IntField()
    title = TextField()
    author = TextField()
    tags = TextField()
    url = TextField()

    class Meta:
        table = "pixiv"
        table_description = "色图数据"

    @classmethod
    async def get_random_illust(
        cls, nsfw: Optional[int] = 0, keywords: Optional[list] = []
    ) -> dict:
        if keywords:
            query = cls.filter(Q(nsfw=nsfw))
            for k in keywords:
                query = query.filter(
                    Q(tags__contains=k) | Q(title__contains=k) | Q(author__contains=k)
                )
            result = await query.values()
            if result:
                num = len(result)
                return result[random.randint(0, num - 1)]
            else:
                return {}
        else:
            result = await cls.filter(Q(nsfw=nsfw)).values()
            num = len(result)
            return result[random.randint(0, num - 1)]

    @classmethod
    async def add_illust(cls, illust: dict) -> None:
        pid = illust["pid"]
        if await cls.check_illust(pid):
            return
        await cls.get_or_create(
            pid=pid,
            uid=illust["uid"],
            nsfw=illust["nsfw"],
            title=illust["title"],
            author=illust["author"],
            tags=illust["tags"],
            url=f"https://www.pixiv.net/artworks/{pid}",
        )

    @classmethod
    async def check_illust(cls, pid: int) -> bool:
        if await Illust.get_or_none(pid=pid):
            return True
        else:
            return False
