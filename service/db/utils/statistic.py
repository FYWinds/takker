"""
Author: FYWindIsland
Date: 2021-08-20 09:37:44
LastEditTime: 2021-08-20 18:26:39
LastEditors: FYWindIsland
Description: 
I'm writing SHIT codes
"""
import json
from typing import Dict
from tortoise.query_utils import Q
from service.db.model.models import Statistic


async def query_status(gid: int) -> Dict[str, Dict[str, int]]:
    q = await Statistic.filter(Q(gid=gid)).values("stat")
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
    if q[0]["illust_stat"] != None:
        return json.loads(str(q[0]["illust_stat"]).replace("'", '"'))
    else:
        return {}


async def set_illust_status(gid: int, kw: str):
    q = await query_illust_statue(gid)
    if q:
        p_kw = q
        if kw in p_kw.keys():
            p_kw[kw] += 1
        else:
            p_kw.update({kw: 1})
        await Statistic.filter(Q(gid=gid)).update(illust_stat=p_kw)
    else:
        await Statistic.filter(Q(gid=gid)).update(illust_stat={kw: 1})
