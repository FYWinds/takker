from argparse import Namespace

from nonebot.log import logger

from api.info import get_group_list
from service.db.utils.perm import set_perm, query_perm
from service.db.utils.plugin_perm import PluginPerm


async def list_perm(args: Namespace) -> str:
    if args.is_superuser:
        pass
    else:
        return "获取群权限等级列表需要超级用户权限"

    message = "群权限等级列表："
    g_list = await get_group_list()
    for group in g_list:
        group_id = group["group_id"]
        perm = await query_perm(id=str(group_id), isGroup=True)
        message = message + "\n" + f"{group_id}: {perm}级"
    return message


async def get_perm(args: Namespace) -> str:
    if args.user or args.group:
        if args.is_superuser:
            pass
        else:
            return "获取指定用户/群权限等级需要超级用户权限"

    if args.user:
        id = args.user[0]
        message = f"用户({id})的权限为: "
        perm = await query_perm(id=str(id), isGroup=False)
        message += f"{perm}级"
        return message
    elif args.group:
        id = args.group[0]
        message = f"群({id})的权限为: "
        perm = await query_perm(id=str(id), isGroup=True)
        message += f"{perm}级"
        return message
    elif args.conv["group"]:
        group_id = args.conv["group"][0]
        message = f"群({group_id})的权限为: "
        perm = await query_perm(id=str(group_id), isGroup=True)
        message += f"{perm}级"
        return message
    else:
        user_id = args.conv["user"][0]
        message = f"用户({user_id})的权限为: "
        perm = await query_perm(id=str(user_id), isGroup=False)
        message += f"{perm}级"
        return message


async def edit_perm(args: Namespace) -> str:
    if args.user:
        if args.is_superuser:
            args.conv |= {"user": args.user}
        else:
            return "修改指定用户/群权限等级需要超级用户权限"
    if args.group:
        if args.is_superuser:
            args.conv |= {"group": args.group}
        else:
            return "修改指定用户/群权限等级需要超级用户权限"
    message = ""
    perm = int(args.perm[0])
    if (args.user or args.group) and (args.is_group):
        return "非私聊，只能修改当前群聊权限等级"
    if args.user:
        for u in args.conv["user"]:
            user_perm = await query_perm(id=str(args.c_user))
            if user_perm > perm:
                await set_perm(id=u, perm=perm)
                message += f"成功设置用户({u})的权限等级为 {perm} 级\n"
            else:
                message += f"您的权限等级({user_perm}级)过低，无法修改用户({u})权限等级为 {perm} 级！\n"
        return message
    elif args.group:
        user_perm = await query_perm(id=args.c_user)
        for g in args.conv["group"]:
            if user_perm > perm:
                await set_perm(id=g, perm=perm, isGroup=True)
                message += f"成功设置群({g})的权限等级为 {perm} 级\n"
            else:
                message += f"您的权限等级({user_perm}级)过低，无法修改群({g})权限等级为 {perm} 级！\n"
        return message
    else:
        user_id = args.conv["user"][0]
        user_perm = await query_perm(id=str(user_id))
        try:
            id = args.conv["group"][0]
            if user_perm > perm:
                await set_perm(id=id, perm=perm, isGroup=True)
                return f"成功设置本群权限等级为 {perm} 级"
            return f"您的权限等级({user_perm}级)过低，无法修改本群权限等级为 {perm} 级！"
        except IndexError:
            return "您无法设置自己的权限等级"


async def edit_plugin_perm(args: Namespace) -> str:
    plugins = args.plugins
    perm = args.perm
    if args.is_group:
        return "请在私聊中修改插件权限"
    if not plugins or not perm:
        return "参数错误"
    current_perms = await PluginPerm.get_all_plugin_perm()
    for plugin in current_perms:
        if plugin in plugins:
            current_perms[plugin] = perm
        else:
            del plugins[plugin]
    await PluginPerm.group_set_plugin_perm(current_perms)

    message = f"插件 {', '.join(plugins)} 的权限成功修改为 {perm} 级"