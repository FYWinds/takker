from typing import Optional
from tortoise.query_utils import Q

from service.db.model.models import Permission


async def query_perm(id: str, isGroup: Optional[bool] = False) -> int:
    """
    :说明: `query_perm`
    > 查询对象权限等级

    :参数:
      * `id: str`: QQ号或群号

    :可选参数:
      * `isGroup: Optional[bool] = False`: 是否是群，默认不是

    :返回:
      - `int`: 权限等级
    """
    if isGroup:
        p = await Permission.filter(Q(id="g" + id)).values("perm")
        if p:
            return p[0]["perm"]
        return 0
    else:
        p = await Permission.filter(Q(id=id)).values("perm")
        if p:
            return p[0]["perm"]
        return 0


async def check_perm(id: str, perm: int, isGroup: Optional[bool] = False) -> bool:
    """
    :说明: `check_perm`
    > 检查对象是否拥有足够权限等级

    :参数:
      * `id: str`: QQ号或群号
      * `perm: int`: 权限等级

    :可选参数:
      * `isGroup: Optional[bool] = False`: 是否是群，默认不是

    :返回:
      - `bool`: 用户等级是否大于给予的权限等级
    """
    p = await query_perm(id=id, isGroup=isGroup)
    if p:
        return p >= perm
    return 0 >= perm


async def set_perm(id: str, perm: int, isGroup: Optional[bool] = False):
    """
    :说明: `set_perm`
    > 修改对象权限等级

    :参数:
      * `id: str`: QQ号或群号
      * `perm: int`: 权限等级

    :可选参数:
      * `isGroup: Optional[bool] = False`: 是否是群，默认不是
    """
    if isGroup:
        query = Permission.filter(Q(id="g" + str(id)))
        if await query.values("perm"):
            await query.update(perm=perm)
        else:
            await Permission.create(id="g" + str(id), perm=perm)
    else:
        query = Permission.filter(Q(id=str(id)))
        if await query.values("perm"):
            await query.update(perm=perm)
        else:
            await Permission.create(id=str(id), perm=perm)


async def remove_perm(id: str, isGroup: Optional[bool] = False):
    """
    :说明: `remove_perm`
    > 删除对象权限条目

    :参数:
      * `id: str`: QQ号或群号

    :可选参数:
      * `isGroup: Optional[bool] = False`: 是否是群，默认不是
    """
    if isGroup:
        await Permission.filter(Q(id="g" + str(id))).delete()
    else:
        await Permission.filter(Q(id=str(id))).delete()
