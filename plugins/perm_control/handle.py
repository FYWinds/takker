from argparse import Namespace

from nonebot.plugin import get_plugin

from db.utils.perm import Perm
from db.utils.plugin_perm import PluginPerm

dash = "-"


async def list_perm(args: Namespace) -> str:
    if args.is_superuser:
        pass
    else:
        return "获取权限等级列表需要超级用户权限"
    if args.group:
        message = f"群权限等级列表：\n{dash*16}"
        g_list = await Perm.get_all_perm(isGroup=True)
        for group in g_list:
            message = message + "\n" + f"{group:10s}: {str(g_list[group]):2s}级"
            message = message + "\n" + f"{dash*16}"
    elif args.user:
        message = f"用户权限等级列表：\n{dash*16}"
        u_list = await Perm.get_all_perm()
        for user in u_list:
            message = message + "\n" + f"{user:10s}: {str(u_list[user]):2s}级"
            message = message + "\n" + f"{dash*16}"
    elif args.plugin:
        message = f"插件权限等级列表：\n{dash*30}"
        p_list = await PluginPerm.get_all_plugin_perm()
        if p_list:
            for plugin in p_list:
                message = message + "\n" + f"{plugin:24s}: {str(p_list[plugin]):2s}级"
                message = message + "\n" + f"{dash*30}"
    else:
        message = "参数错误"
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
        perm = await Perm.query_perm(id=str(id), isGroup=False)
        message += f"{perm}级"
        return message
    elif args.group:
        id = args.group[0]
        message = f"群({id})的权限为: "
        perm = await Perm.query_perm(id=str(id), isGroup=True)
        message += f"{perm}级"
        return message
    elif args.conv["group"]:
        group_id = args.conv["group"][0]
        message = f"群({group_id})的权限为: "
        perm = await Perm.query_perm(id=str(group_id), isGroup=True)
        message += f"{perm}级"
        return message
    else:
        user_id = args.conv["user"][0]
        message = f"用户({user_id})的权限为: "
        perm = await Perm.query_perm(id=str(user_id), isGroup=False)
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
            user_perm = await Perm.query_perm(id=str(args.c_user))
            if user_perm > perm:
                await Perm.set_perm(id=u, perm=perm)
                message += f"成功设置用户({u})的权限等级为 {perm} 级\n"
            else:
                message += f"您的权限等级({user_perm}级)过低，无法修改用户({u})权限等级为 {perm} 级！\n"
        return message
    elif args.group:
        user_perm = await Perm.query_perm(id=args.c_user)
        for g in args.conv["group"]:
            if user_perm > perm:
                await Perm.set_perm(id=g, perm=perm, isGroup=True)
                message += f"成功设置群({g})的权限等级为 {perm} 级\n"
            else:
                message += f"您的权限等级({user_perm}级)过低，无法修改群({g})权限等级为 {perm} 级！\n"
        return message.strip()
    else:
        user_id = args.conv["user"][0]
        user_perm = await Perm.query_perm(id=str(user_id))
        try:
            id = args.conv["group"][0]
            if user_perm > perm:
                await Perm.set_perm(id=id, perm=perm, isGroup=True)
                return f"成功设置本群权限等级为 {perm} 级"
            return f"您的权限等级({user_perm}级)过低，无法修改本群权限等级为 {perm} 级！"
        except IndexError:
            return "您无法设置自己的权限等级"


async def edit_plugin_perm(args: Namespace) -> str:
    plugins: list = args.plugins
    edited_plugins: list = []
    perm = args.perm
    if not plugins or not perm:
        return "参数错误"
    perm = int(perm[0])
    current_perms = await PluginPerm.get_all_plugin_perm()
    if current_perms:
        for plugin in current_perms:
            if plugin in plugins:
                current_perms[plugin] = perm
                edited_plugins.append(plugin)
        await PluginPerm.group_set_plugin_perm(current_perms)
    message = f"插件 {', '.join(edited_plugins)} 的权限成功修改为 {perm} 级"
    return message


async def reset_perm(args: Namespace) -> str:
    if args.is_superuser:
        if args.user:
            for u in args.user:
                await Perm.set_perm(id=u, perm=0)
            return f"成功重置用户 {', '.join(args.user)} 的权限等级为 0 级"
        elif args.group:
            for g in args.group:
                await Perm.set_perm(id=g, perm=0, isGroup=True)
            return f"成功重置群 {', '.join(args.group)} 的权限等级为 0 级"
        elif args.plugin:
            plugin_perms = await PluginPerm.get_all_plugin_perm()
            reseted_plugins = []
            if plugin_perms:
                for p in args.plugin:
                    if p in plugin_perms:
                        plugin = get_plugin(p)
                        assert plugin is not None
                        plugin_info = getattr(plugin.module, "__plugin_info__", {})
                        plugin_perms[p] = plugin_info.get("permission", 5)
                        reseted_plugins.append(p)
                await PluginPerm.group_set_plugin_perm(plugin_perms)
            return f"成功重置插件 {', '.join(reseted_plugins)} 的权限等级为其默认等级"
        else:
            return "请指定用户或群或插件"
    else:
        return "重置权限等级需要超级用户权限"
