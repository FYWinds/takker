from typing import Optional

from service.db.models.config import BotConfig


class PluginPerm:
    @staticmethod
    async def get_plugin_perm(name: str) -> Optional[int]:
        config = await BotConfig.get_or_none(id=1)
        if config and config.plugin_perms:
            perms = config.plugin_perms
            if name in perms:
                return perms[name]
        return None

    @staticmethod
    async def set_plugin_perm(name: str, perm: int) -> None:
        config = await BotConfig.get_or_none(id=1)
        if config and config.plugin_perms:
            perms = config.plugin_perms
            perms[name] = perm
            config.plugin_perms = perms
            await config.save()

    @staticmethod
    async def remove_plugin_perm(name: str) -> None:
        config = await BotConfig.get_or_none(id=1)
        if config and config.plugin_perms:
            perms = config.plugin_perms
            if name in perms:
                del perms[name]
                config.plugin_perms = perms
                await config.save()

    @staticmethod
    async def get_all_plugin_perm() -> Optional[dict[str, int]]:
        config = await BotConfig.get_or_none(id=1)
        if config and config.plugin_perms:
            return config.plugin_perms
        return None

    @staticmethod
    async def group_set_plugin_perm(plugin_perms: dict[str, int]) -> None:
        await BotConfig.update_or_create(id=1, defaults={"plugin_perms": plugin_perms})
