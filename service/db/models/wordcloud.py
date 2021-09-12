import time
from typing import Union

from tortoise.fields import TextField, BigIntField
from tortoise.models import Model
from tortoise.query_utils import Q


class Wordcloud(Model):
    """群热词词云"""

    gid = BigIntField()
    uid = BigIntField()
    time = BigIntField()
    msg = TextField(null=True)
    msg_seg = TextField(null=True)

    class Meta:
        table = "wordcloud"
        table_description = "热词词云数据"
        indexes = ("gid",)

    @classmethod
    async def get_words(cls, gid: Union[int, str], after_time: int) -> list:
        q = await cls.filter(Q(gid=int(gid)) & Q(time__gte=after_time)).values("msg_seg")
        try:
            msg_seg = []
            for i in q:
                msg_seg += [i["msg_seg"]]
            return msg_seg
        except:
            return []

    @classmethod
    async def log_words(cls, gid: Union[int, str], uid: int, msg: str, msg_seg: str):
        await cls.create(
            gid=int(gid), uid=uid, time=int(time.time()), msg=msg, msg_seg=msg_seg
        )

    @classmethod
    async def delete_history(cls):
        ptime = int(time.time()) - 60 * 60 * 24 * 365
        await cls.filter(Q(time__lte=ptime)).delete()
