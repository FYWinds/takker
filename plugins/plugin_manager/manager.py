from nonebot.log import logger
from configs.config import HIDDEN_PLUGINS
from nonebot.plugin import get_plugin, get_loaded_plugins
from service.db.utils.plugin_manager import set_plugin_status, query_plugin_status


async def get_plugin_list(
    conv={"user": [], "group": []}, perm: int = 0
) -> dict[str, bool]:
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
                result |= {p: bool(plugin_list[p])}
    return result


async def ban_plugin(
    conv={"user": [], "group": []}, plugin: list[str] = [], perm: int = 0
) -> dict[str, bool]:
    plugin_list: dict[str, bool] = {}
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
                    plugin_list |= {p: False}
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
                    plugin_list |= {p: False}
                    await set_plugin_status(str(u), plugin_list, isGroup=False)
    return result


async def unban_plugin(
    conv={"user": [], "group": []}, plugin: list[str] = [], perm: int = 0
) -> dict[str, bool]:
    plugin_list: dict[str, bool] = {}
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
                    plugin_list |= {p: True}
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
                    plugin_list |= {p: True}
                    await set_plugin_status(str(u), plugin_list, isGroup=False)
    return result
