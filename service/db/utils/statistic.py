import json
from typing import Dict
from tortoise.query_utils import Q
from service.db.model.models import Statistic


async def query_status(gid: int) -> Dict[str, Dict[str, int]]:
    q = await Statistic.filter(Q(gid=gid)).values("stat")
    if not q:
        return {}
    if q[0]["stat"] != None:
        return json.loads(str(q[0]["stat"]).replace("'", '"'))
    else:
        return {}


async def set_status(gid: int, stat: Dict[str, Dict[str, int]]):
    query = Statistic.filter(Q(gid=gid))
    if await query.values():
        await query.update(stat=str(stat))
    else:
        await Statistic.create(gid=gid, stat=str(stat))


illust: Dict[str, int]


async def query_illust_statue(gid: int) -> Dict[str, int]:
    q = await Statistic.filter(Q(gid=gid)).values("illust_stat")
    if not q:
        return {}
    if q[0]["illust_stat"] != None:
        return json.loads(str(q[0]["illust_stat"]).replace("'", '"'))
    else:
        return {}


async def set_illust_status(gid: int, kw: list):
    q = await query_illust_statue(gid)
    for k in kw:
        if q:
            p_kw = q
            if k in p_kw.keys():
                p_kw[k] += 1
            else:
                p_kw.update({k: 1})
            await Statistic.filter(Q(gid=gid)).update(illust_stat=p_kw)
        else:
            await Statistic.filter(Q(gid=gid)).update(illust_stat={k: 1})
