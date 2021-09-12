from typing import Union

from service.db.models.config import UserConfig, GroupConfig


async def query_plugin_status(
    id: Union[int, str], isGroup: bool = False
) -> dict[str, bool]:
    """
    :说明: `query_plugin_status`
    > 获取对象插件状态数据

    :参数:
      * `id: Union[int, str]`: QQ号或群号
      * `isGroup: bool = False`: 是否是群，默认不是

    :返回:
      - `dict`: 插件状态数据
    """
    if isinstance(id, str):
        id = int(id)
    if isGroup:
        p = await GroupConfig.get_or_none(gid=id)
    else:
        p = await UserConfig.get_or_none(uid=id)
    if p:
        return p.plugin_status
    else:
        return {}


async def set_plugin_status(
    id: Union[int, str], status: dict[str, bool], isGroup: bool = False
):
    """
    :说明: `set_plugin_status`
    > 修改对象插件状态数据

    :参数:
      * `id: Union[int, str]`: QQ号或群号
      * `status: dict`: 插件状态数据
      * `isGroup: bool = False`: 是否是群，默认不是
    """
    if isinstance(id, str):
        id = int(id)
    if isGroup:
        await GroupConfig.update_or_create(
            gid=id, defaults={"plugin_status": status}
        )
    else:
        await UserConfig.update_or_create(
            uid=id, defaults={"plugin_status": status}
        )
