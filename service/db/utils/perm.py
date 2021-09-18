from typing import Union, Optional

from tortoise.query_utils import Q

from service.db.models.config import UserConfig, GroupConfig


async def query_perm(id: Union[int, str], isGroup: Optional[bool] = False) -> int:
    """
    :说明: `query_perm`
    > 查询对象权限等级

    :参数:
      * `id: Union[int, str]`: QQ号或群号

    :可选参数:
      * `isGroup: Optional[bool] = False`: 是否是群，默认不是

    :返回:
      - `int`: 权限等级
    """
    if isGroup:
        p = await GroupConfig.get_or_none(gid=int(id))
    else:
        p = await UserConfig.get_or_none(uid=int(id))

    if p and p.perm:
        return p.perm
    else:
        return 0


async def check_perm(
    id: Union[int, str], perm: int, isGroup: Optional[bool] = False
) -> bool:
    """
    :说明: `check_perm`
    > 检查对象是否拥有足够权限等级

    :参数:
      * `id: Union[int, str]`: QQ号或群号
      * `perm: int`: 权限等级

    :可选参数:
      * `isGroup: Optional[bool] = False`: 是否是群，默认不是

    :返回:
      - `bool`: 用户等级是否大于给予的权限等级
    """
    p = await query_perm(id, isGroup)
    if p:
        return p >= perm
    return 0 >= perm


async def set_perm(
    id: Union[int, str], perm: int, isGroup: Optional[bool] = False
) -> None:
    """
    :说明: `set_perm`
    > 修改对象权限等级

    :参数:
      * `id: Union[int, str]`: QQ号或群号
      * `perm: int`: 权限等级

    :可选参数:
      * `isGroup: Optional[bool] = False`: 是否是群，默认不是
    """
    if isGroup:
        await GroupConfig.update_or_create(gid=int(id), defaults={"perm": perm})
    else:
        await UserConfig.update_or_create(uid=int(id), defaults={"perm": perm})


async def remove_perm(id: Union[int, str], isGroup: Optional[bool] = False) -> None:
    """
    :说明: `remove_perm`
    > 删除对象权限条目

    :参数:
      * `id: Union[int, str]`: QQ号或群号

    :可选参数:
      * `isGroup: Optional[bool] = False`: 是否是群，默认不是
    """
    id = int(id) if isinstance(id, str) else id
    if isGroup:
        await GroupConfig.filter(Q(id=id)).delete()
    else:
        await UserConfig.filter(Q(id=id)).delete()
