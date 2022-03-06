from typing import Union

from db.models.config import UserConfig, GroupConfig


class PluginManager:
    @staticmethod
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
        if isGroup:
            p = await GroupConfig.get_or_none(gid=int(id))
        else:
            p = await UserConfig.get_or_none(uid=int(id))
        if p and p.plugin_status:
            return p.plugin_status
        else:
            return {}

    @staticmethod
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
        if isGroup:
            await GroupConfig.update_or_create(
                gid=int(id), defaults={"plugin_status": status}
            )
        else:
            await UserConfig.update_or_create(
                uid=int(id), defaults={"plugin_status": status}
            )
