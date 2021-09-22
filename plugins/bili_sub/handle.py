from argparse import Namespace

from service.db.models.bs import Bili_sub

DB = Bili_sub()

_blank = "    "


async def ls(args: Namespace) -> str:
    sub_list: dict[str, dict[int, dict[int, str]]] = {"group": {}, "user": {}}

    # 获取所有会话的订阅列表
    if args.all:
        data = await DB.get_all_sub()
        for group in data["group"]:
            sub_list["group"] |= {group: {}}
            sub = data["group"][group]
            for s in sub:
                sub_list["group"][group] |= {s: sub[s]}
        for user in data["user"]:
            sub_list["user"] |= {user: {}}
            sub = data["user"][user]
            for s in sub:
                sub_list["user"][user] |= {s: sub[s]}

    # 私聊会话
    elif args.is_user:
        # 私聊控制其他群组
        if args.group:
            for group in args.group:
                sub = await DB.get_sub(group, isGroup=True)
                sub_list["group"] |= {group: {}}
                for s in sub:
                    sub_list["group"][group] |= {s: sub[s]}
        # 私聊控制其他用户
        if args.user:
            for user in args.user:
                sub = await DB.get_sub(user)
                sub_list["user"] |= {user: {}}
                for s in sub:
                    sub_list["user"][user] |= {s: sub[s]}
        # 私聊控制当前私聊
        if not args.user and not args.group:
            user = args.conv["user"]
            sub = await DB.get_sub(user)
            sub_list["user"] |= {user: {}}
            for s in sub:
                sub_list["user"][user] |= {s: sub[s]}

    # 群聊仅控制当前群聊
    elif args.is_group:
        if args.user or args.group:
            return "请在私聊中对其他会话进行操作"
        group = args.conv["group"]
        sub = await DB.get_sub(group, isGroup=True)
        sub_list["group"] |= {group: {}}
        for s in sub:
            sub_list["group"][group] |= {s: sub[s]}

    # 构造消息内容
    """
    订阅列表
    群 xxxxxxx 中:
    萝卜吃米洛(5007752):
        动态: 开  直播: 开  全体: 关
    用户 xxxxxxx 中:
    萝卜吃米洛(5007752)
        动态: 开  直播: 开  全体: 关
    """
    message: list = ["订阅列表"]
    if sub_list["group"]:
        for group in sub_list["group"]:
            message.append(f"群 {group} 中:")
            if not sub_list["group"][group]:
                message.append("暂无订阅")
                continue
            for sub in sub_list["group"][group]:
                sub_name = sub_list["group"][group][sub]
                message.append(f"{_blank}{sub_name}({sub})")
                sub_info = await DB.get_settings(id=group, bid=sub, isGroup=True)
                settings = convert_settings(sub_info)
                message.append(f"{_blank}{_blank}{settings}")
    if sub_list["user"]:
        for user in sub_list["user"]:
            message.append(f"用户 {user} 中:")
            if not sub_list["user"][user]:
                message.append("暂无订阅")
                continue
            for sub in sub_list["user"][user]:
                sub_name = sub_list["user"][user][sub]
                message.append(f"{_blank}{sub_name}({sub})")
                sub_info = await DB.get_settings(id=user, bid=sub)
                settings = convert_settings(sub_info)
                message.append(f"{_blank}{_blank}{settings}")
    message_s: str = "\n".join(message)
    return message_s


async def add(args: Namespace) -> str:
    message: str = ""
    # 私聊会话
    if args.is_user:
        # 私聊控制其他群组
        if args.group:
            message += "群"
            for group in args.group:
                for bid in args.bid:
                    message += f" {group} 中:\n"
                    if not await DB.add_record(id=group, bid=bid, isGroup=True):
                        message += f"UP {bid} 添加失败，请检查是否重复添加或错将直播房间号当作用户ID\n"
                    else:
                        name = await DB.get_user_name(bid)
                        message += f"  UP {name}({bid}) 添加成功\n"
        # 私聊控制其他用户
        if args.user:
            message += "用户"
            for user in args.user:
                for bid in args.bid:
                    message += f" {user} 中:\n"
                    if not await DB.add_record(id=user, bid=bid):
                        message += f"UP {bid} 添加失败，请检查是否重复添加或错将直播房间号当作用户ID\n"
                    else:
                        name = await DB.get_user_name(bid)
                        message += f"  UP {name}({bid}) 添加成功\n"
        # 私聊控制当前私聊
        if not args.user and not args.group:
            message += "用户"
            user = args.conv["user"]
            message += f" {user} 中:\n"
            for bid in args.bid:
                if not await DB.add_record(id=user, bid=bid):
                    message += f"UP {bid} 添加失败，请检查是否重复添加或错将直播房间号当作用户ID\n"
                else:
                    name = await DB.get_user_name(bid)
                    message += f"  UP {name}({bid}) 添加成功\n"

    # 群聊仅控制当前群聊
    elif args.is_group:
        if args.user or args.group:
            return "请在私聊中对其他会话进行操作"
        group = args.conv["group"]
        for bid in args.bid:
            if not await DB.add_record(id=group, bid=bid, isGroup=True):
                message += f"UP {bid} 添加失败，请检查是否重复添加或错将直播房间号当作用户ID\n"
            else:
                name = await DB.get_user_name(bid)
                message += f"  UP {name}({bid}) 添加成功\n"
    return message


async def remove(args: Namespace) -> str:
    message: str = ""
    # 私聊会话
    if args.is_user:
        # 私聊控制其他群组
        if args.group:
            message += "群"
            for group in args.group:
                for bid in args.bid:
                    message += f" {group} 中:\n"
                    if not await DB.remove_record(id=group, bid=bid, isGroup=True):
                        message += f"UP {bid} 删除失败，请检查是否误写或错将直播房间号当作用户ID\n"
                    else:
                        name = await DB.get_user_name(bid)
                        message += f"  UP {name}({bid}) 删除成功\n"
        # 私聊控制其他用户
        if args.user:
            message += "用户"
            for user in args.user:
                for bid in args.bid:
                    message += f" {user} 中:\n"
                    if not await DB.remove_record(id=user, bid=bid):
                        message += f"UP {bid} 删除失败，请检查是否误写或错将直播房间号当作用户ID\n"
                    else:
                        name = await DB.get_user_name(bid)
                        message += f"  UP {name}({bid}) 删除成功\n"
        # 私聊控制当前私聊
        if not args.user and not args.group:
            message += "用户"
            user = args.conv["user"]
            message += f" {user} 中:\n"
            for bid in args.bid:
                if not await DB.remove_record(id=user, bid=bid):
                    message += f"UP {bid} 删除失败，请检查是否误写或错将直播房间号当作用户ID\n"
                else:
                    name = await DB.get_user_name(bid)
                    message += f"  UP {name}({bid}) 删除成功\n"

    # 群聊仅控制当前群聊
    elif args.is_group:
        if args.user or args.group:
            return "请在私聊中对其他会话进行操作"
        group = args.conv["group"]
        for bid in args.bid:
            if not await DB.remove_record(id=group, bid=bid, isGroup=True):
                message += f"UP {bid} 删除失败，请检查是否误写或错将直播房间号当作用户ID\n"
            else:
                name = await DB.get_user_name(bid)
                message += f"  UP {name}({bid}) 删除成功\n"
    return message


async def settings(args: Namespace) -> str:
    async def edit(id, bid, isGroup: bool = False) -> None:
        if args.at:
            await DB.edit_settings(id=id, bid=bid, set="at", isGroup=isGroup)
        if args.live:
            await DB.edit_settings(id=id, bid=bid, set="live", isGroup=isGroup)
        if args.dynamic:
            await DB.edit_settings(id=id, bid=bid, set="dynamic", isGroup=isGroup)

    message = ""

    # 私聊会话
    if args.is_user:
        # 私聊控制其他群组
        if args.group:
            message += f"群 {', '.join(args.group)} 中:"
            for group in args.group:
                for bid in args.bid:
                    await edit(group, bid, isGroup=True)
        # 私聊控制其他用户
        if args.user:
            message += f"用户 {', '.join(args.user)} 中:"
            for user in args.user:
                for bid in args.bid:
                    await edit(user, bid)
        # 私聊控制当前私聊
        if not args.user and not args.group:
            user = args.conv["user"]
            message += f"用户 {user} 中:"
            for bid in args.bid:
                await edit(user, bid)

    # 群聊仅控制当前群聊
    elif args.is_group:
        if args.user or args.group:
            return "请在私聊中对其他会话进行操作"
        group = args.conv["group"]
        message += f"群 {group} 中:"
        for bid in args.bid:
            await edit(group, bid, isGroup=True)

    message += f"\n  UP {', '.join(args.bid)} :"
    message += "\n全体状态 " if args.at else ""
    message += "\n直播状态 " if args.live else ""
    message += "\n动态状态 " if args.dynamic else ""
    message += "\n切换成功"

    return message


def convert_settings(settings: dict[str, bool]) -> str:
    """
    :说明: `convert_settings`
    > 转换设置项至文字

    :参数:
      * `settings: dict[str, bool]`: 设置项 格式为service.db.models.hb.Bili_sub().get_settings()的返回值

    :返回:
      - `str`: 转换后的文字 格式为 动态: 开  直播: 开  全体: 关
    """
    message = ""
    message += f"动态: {'开' if settings['dynamic'] else '关'}  "
    message += f"直播: {'开' if settings['live'] else '关'}  "
    message += f"全体: {'开' if settings['at'] else '关'}"
    return message
