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
            if plugin.name in HIDDEN_PLUGINS:
                continue
            try:
                plugin_perm = int(plugin.module.__getattribute__("__permission__"))
            except:
                plugin_perm = 5
            if plugin_perm <= perm:
                result|={p: bool(plugin_list[p])}
    return result


async def ban_plugin(
    conv={"user": [], "group": []}, plugin: List[str] = [], perm: int = 0
) -> Dict[str, bool]:
    plugin_list: Dict[str, bool] = {}
    result = {}
    all_plugin_list = await get_plugin_list(conv, perm)
    if conv["group"]:
        for g in conv["group"]:
            for p in plugin:
                result[p] = False
                if p in all_plugin_list:
                    result[p] = True
                    try:
                        plugin_perm = int(get_plugin(p).module.__getattribute__("__permission__"))  # type: ignore
                    except:
                        plugin_perm = 5
                    if plugin_perm > perm:
                        result[p] = False
                        continue
                    plugin_list|={p: False}
                    await set_plugin_status(str(g), plugin_list, isGroup=True)
    else:
        for u in conv["user"]:
            for p in plugin:
                result[p] = False
                if p in all_plugin_list:
                    result[p] = True
                    try:
                        plugin_perm = int(get_plugin(p).module.__getattribute__("__permission__"))  # type: ignore
                    except:
                        plugin_perm = 5
                    if plugin_perm > perm:
                        result[p] = False
                        continue
                    plugin_list|={p: False}
                    await set_plugin_status(str(u), plugin_list, isGroup=False)
    return result


async def unban_plugin(
    conv={"user": [], "group": []}, plugin: List[str] = [], perm: int = 0
) -> Dict[str, bool]:
    plugin_list: Dict[str, bool] = {}
    all_plugin_list = await get_plugin_list(conv, perm)
    result = {}
    if conv["group"]:
        for g in conv["group"]:
            for p in plugin:
                result[p] = False
                if p in all_plugin_list:
                    result[p] = True
                    try:
                        plugin_perm = int(get_plugin(p).module.__getattribute__("__permission__"))  # type: ignore
                    except:
                        plugin_perm = 5
                    if plugin_perm > perm:
                        result[p] = False
                        continue
                    plugin_list|={p: True}
                    await set_plugin_status(str(g), plugin_list, isGroup=True)
    else:
        for u in conv["user"]:
            for p in plugin:
                result[p] = False
                if p in all_plugin_list:
                    result[p] = True
                    try:
                        plugin_perm = int(get_plugin(p).module.__getattribute__("__permission__"))  # type: ignore
                    except:
                        plugin_perm = 5
                    if plugin_perm > perm:
                        result[p] = False
                        continue
                    plugin_list|={p: True}
                    await set_plugin_status(str(u), plugin_list, isGroup=False)
    return result
