from typing import Dict, List, Optional
from nonebot.log import logger
from nonebot.plugin import get_loaded_plugins, get_plugin

from configs.config import HIDDEN_PLUGINS
from service.db.utils.plugin_manager import query_plugin_status, set_plugin_status


async def get_plugin_list(
    conv={"user": [], "group": []}, perm: int = 0
) -> Dict[str, bool]:
    if conv["group"]:
        plugin_list = await query_plugin_status(id=str(conv["group"][0]), isGroup=True)
    else:
        plugin_list = await query_plugin_status(id=str(conv["user"][0]))
    result = {}
    for p in list(plugin_list.keys()):
        plugin = get_plugin(p)
        if plugin:
            plugin_perm = int(plugin.module.__getattribute__("__permission__"))
            if plugin_perm <= perm:
                result.update({p: bool(plugin_list[p])})
    print(result)
    return result


async def ban_plugin(
    conv={"user": [], "group": []}, plugin: List[str] = [], perm: int = 0
) -> Dict[str, bool]:
    plugin_list: Dict[str, bool] = {}
    pass
    result = {}
    for p in plugin:
        result[p] = False
        if p in await get_plugin_list(conv, perm):
            result[p] = True
            plugin_perm = int(get_plugin(p).module.__getattribute__("__permission__"))  # type: ignore
            if plugin_perm > perm:
                result[p] = False
                continue
            if conv["group"]:
                plugin_list.update({p: False})
                await set_plugin_status(
                    str(conv["group"][0]), plugin_list, isGroup=True
                )
            else:
                plugin_list.update({p: False})
                await set_plugin_status(
                    str(conv["user"][0]), plugin_list, isGroup=False
                )
    return result


async def unban_plugin(
    conv={"user": [], "group": []}, plugin: List[str] = [], perm: int = 0
) -> Dict[str, bool]:
    plugin_list: Dict[str, bool] = {}
    pass
    result = {}
    for p in plugin:
        result[p] = False
        if p in await get_plugin_list(conv, perm):
            result[p] = True
            plugin_perm = int(get_plugin(p).module.__getattribute__("__permission__"))  # type: ignore
            if plugin_perm > perm:
                result[p] = False
                continue
            if conv["group"]:
                plugin_list.update({p: True})
                await set_plugin_status(
                    str(conv["group"][0]), plugin_list, isGroup=True
                )
            else:
                plugin_list.update({p: True})
                await set_plugin_status(
                    str(conv["user"][0]), plugin_list, isGroup=False
                )
    return result
