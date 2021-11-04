from typing import Optional

from db.models.config import BotConfig


class PluginPerm:
    @staticmethod
    async def get_plugin_perm(name: str) -> int:
        """
        :说明: `get_plugin_perm`
        > 获取某个插件的权限等级

        :参数:
          * `name: str`: 插件名称

        :返回:
          - `int`: 权限等级
        """
        config = await BotConfig.get_or_none(id=1)
        if config and config.plugin_perms:
            perms = config.plugin_perms
            if name in perms:
                return perms[name]
        return 5

    @staticmethod
    async def set_plugin_perm(name: str, perm: int) -> None:
        """
        :说明: `set_plugin_perm`
        > 设置某个插件的权限等级

        :参数:
          * `name: str`: 插件名称
          * `perm: int`: 权限等级
        """
        config = await BotConfig.get_or_none(id=1)
        if config and config.plugin_perms:
            perms = config.plugin_perms
            perms[name] = perm
            config.plugin_perms = perms
            await config.save()

    @staticmethod
    async def remove_plugin_perm(name: str) -> None:
        """
        :说明: `remove_plugin_perm`
        > 移除某一插件权限

        :参数:
          * `name: str`: 插件名称
        """
        config = await BotConfig.get_or_none(id=1)
        if config and config.plugin_perms:
            perms = config.plugin_perms
            if name in perms:
                del perms[name]
                config.plugin_perms = perms
                await config.save()

    @staticmethod
    async def get_all_plugin_perm() -> Optional[dict[str, int]]:
        """
        :说明: `get_all_plugin_perm`
        > 获取所有插件权限列表

        :返回:
          - `Optional[dict[str, int]]`: 插件权限列表
        """
        config = await BotConfig.get_or_none(id=1)
        if config and config.plugin_perms:
            return config.plugin_perms
        return None

    @staticmethod
    async def group_set_plugin_perm(plugin_perms: dict[str, int]) -> None:
        """
        :说明: `group_set_plugin_perm`
        > 覆盖设置插件权限列表

        :参数:
          * `plugin_perms: dict[str, int]`: 插件权限列表
        """
        await BotConfig.update_or_create(id=1, defaults={"plugin_perms": plugin_perms})
