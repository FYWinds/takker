"""
Author: FYWindIsland
Date: 2021-08-14 11:47:29
LastEditTime: 2021-08-21 15:28:25
LastEditors: FYWindIsland
Description: 
I'm writing SHIT codes
"""
from argparse import Namespace

from nonebot.log import logger

from api.info import get_group_list
from service.db.utils.perm import query_perm, set_perm


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


async def edit_perm(args: Namespace):
    if args.user:
        if args.is_superuser:
            args.conv.update({"user": args.user})
        else:
            return "修改指定用户/群权限等级需要超级用户权限"
    if args.group:
        if args.is_superuser:
            args.conv.update({"group": args.group})
        else:
            return "修改指定用户/群权限等级需要超级用户权限"
    message = ""
    perm = int(args.perm[0])
    if (args.user or args.group) and (args.is_group):
        return f"非私聊，只能修改当前群聊权限等级"
    if args.user:
        for u in args.conv["user"]:
            user_perm = await query_perm(id=str(u))
            if user_perm > perm:
                await set_perm(id=u, perm=perm)
                message += f"成功设置用户({u})的权限等级为 {perm} 级\n"
            else:
                message += f"您的权限等级({user_perm}级)过低，无法修改用户({u})权限等级为 {perm} 级！\n"
        return message
    elif args.group:
        user_id = args.conv["user"][0]
        user_perm = await query_perm(id=str(user_id))
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
        except:
            return f"您无法设置自己的权限等级"
