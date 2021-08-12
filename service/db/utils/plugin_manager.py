import json
from typing import Optional, Dict
from tortoise.query_utils import Q

from service.db.model.models import Plugin


async def query_plugin_status(
    id: str, isGroup: Optional[bool] = False
) -> Dict[str, bool]:
    """
    :说明: `query_plugin_status`
    > 获取对象插件状态数据

    :参数:
      * `id: str`: QQ号或群号

    :可选参数:
      * `isGroup: Optional[bool] = False`: 是否是群，默认不是

    :返回:
      - `dict`: 插件状态数据
    """
    if isGroup:
        p = await Plugin.filter(Q(id="g" + id)).values("status")
    else:
        p = await Plugin.filter(Q(id=id)).values("status")
    if p:
        return eval(p[0]["status"].replace("'", '"'))
    else:
        return {}


async def set_plugin_status(
    id: str, status: Dict[str, bool], isGroup: Optional[bool] = False
):
    """
    :说明: `set_plugin_status`
    > 修改对象插件状态数据

    :参数:
      * `id: str`: QQ号或群号
      * `status: dict`: 插件状态数据

    :可选参数:
      * `isGroup: Optional[bool] = False`: 是否是群，默认不是
    """
    if isGroup:
        query = Plugin.filter(Q(id="g" + id))
        if await query.values("status"):
            await query.update(status=str(status))
        else:
            await Plugin.create(id="g" + id, status=str(status))
    else:
        query = Plugin.filter(Q(id=id))
        if await query.values("status"):
            await query.update(status=str(status))
        else:
            await Plugin.create(id=id, status=str(status))
