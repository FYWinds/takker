import json
from typing import Union

from tortoise.fields import TextField, BigIntField
from tortoise.models import Model


class Statistic(Model):
    """插件调用数据"""

    gid = BigIntField(pk=True)
    stat = TextField(null=True)
    illust_stat = TextField(null=True)

    class Meta:
        table = "statistic"
        table_description = "插件调用数据"
        indexes = ("gid",)

    @classmethod
    async def query_status(cls, gid: Union[int, str]) -> dict[str, dict[str, int]]:
        q = await cls.get_or_none(gid=int(gid))
        if not q:
            return {}
        if q.stat != None:
            return json.loads(str(q.stat).replace("'", '"'))
        else:
            return {}

    @classmethod
    async def set_status(cls, gid: Union[int, str], stat: dict[str, dict[str, int]]):
        await cls.update_or_create(gid=int(gid), defaults={"stat": stat})

    @classmethod
    async def query_illust_statue(cls, gid: Union[int, str]) -> dict[str, int]:
        q = await cls.get_or_none(gid=int(gid))
        if not q:
            return {}
        if q.illust_stat != None:
            return json.loads(str(q.illust_stat).replace("'", '"'))
        else:
            return {}

    @classmethod
    async def set_illust_status(cls, gid: Union[int, str], kw: list):
        gid = int(gid)
        q = await cls.query_illust_statue(gid)
        for k in kw:
            if q:
                p_kw = q
                if k in p_kw.keys():
                    p_kw[k] += 1
                else:
                    p_kw.update({k: 1})
                await cls.update_or_create(gid=gid, defaults={"illust_stat":p_kw})
            else:
                await cls.update_or_create(gid=gid, defaults={"illust_stat":{k: 1}})
