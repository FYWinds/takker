from typing import Dict
from argparse import Namespace

from nonebot.log import logger
from service.db.utils.perm import query_perm
from service.db.utils.plugin_manager import query_plugin_status, set_plugin_status

from .manager import ban_plugin, get_plugin_list, unban_plugin


async def handle_ls(args: Namespace) -> str:
    message = ""
    plugin_list = {}
    if args.user or args.group:
        if args.is_superuser:
            args.conv = {"user": args.user, "group": args.group}
        else:
            return "获取指定会话的插件列表需要超级用户权限！"
    for t in args.conv:
        for i in args.conv[t]:
            message = f"{'用户' if t == 'user' else '群'}({i}) 的插件列表：\n"
            perm = await query_perm(id=str(i), isGroup=True if t == "group" else False)
            plugin_list = await get_plugin_list(args.conv, perm)
    message += "\n".join(f"[{'o' if plugin_list[p] else 'x'}] {p}" for p in plugin_list)
    return message


async def handle_ban(args: Namespace):
    permission = await query_perm(id=str(args.conv["user"][0]))
    plugin = await get_plugin_list(args.conv, permission)
    if args.all:
        args.plugin = list(p for p in plugin)
    if args.reverse:
        args.plugin = list(filter(lambda p: p not in args.plugin, plugin))
    result: Dict[str, bool]
    result = {}
    if not args.is_superuser:
        for p in plugin:
            if p in args.plugin and not plugin[p]:
                args.plugin.pop(p)  # type: ignore
                result[p] = False

    if args.user or args.group:
        if args.is_superuser:
            args.conv = {"user": args.user, "group": args.group}
        else:
            return "管理指定会话的插件需要超级用户权限！"

    result.update(await ban_plugin(args.conv, args.plugin, permission))

    message = ""
    if args.conv["group"]:
        message += "群"
        message += ",".join(str(i) for i in args.conv["group"])
    else:
        message += "用户"
        message += ",".join(str(i) for i in args.conv["user"])
    message += "中："

    for p in result:
        message += "\n"
        if result[p]:
            message += f"插件 {p} 禁用成功！"
        else:
            message += f"插件 {p} 不存在或您的权限不足！"
    return message


async def handle_unban(args: Namespace):
    perm = await query_perm(id=str(args.conv["user"][0]))
    plugin = await get_plugin_list(args.conv, perm)
    if args.all:
        args.plugin = list(p for p in plugin)
    if args.reverse:
        args.plugin = list(filter(lambda p: p not in args.plugin, plugin))
    result: Dict[str, bool]
    result = {}
    if not args.is_superuser:
        for p in plugin:
            if p in args.plugin and not plugin[p]:
                args.plugin.pop(p)  # type: ignore
                result[p] = False

    if args.user or args.group:
        if args.is_superuser:
            args.conv = {"user": args.user, "group": args.group}
        else:
            return "管理指定会话的插件需要超级用户权限！"

    result.update(await unban_plugin(args.conv, args.plugin, perm))

    message = ""
    if args.conv["group"]:
        message += "群"
        message += ",".join(str(i) for i in args.conv["group"])
    else:
        message += "用户"
        message += ",".join(str(i) for i in args.conv["user"])
    message += "中："

    for p in result:
        message += "\n"
        if result[p]:
            message += f"插件 {p} 启用成功！"
        else:
            message += f"插件 {p} 不存在或您的权限不足！"
    return message
