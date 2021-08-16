"""
Author: FYWindIsland
Date: 2021-08-14 11:47:29
LastEditTime: 2021-08-15 10:10:55
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
    else:
        if args.conv["group"]:
            group_id = args.conv["group"][0]
            message = f"群({group_id})的权限为: "
            perm = await query_perm(id=str(group_id), isGroup=True)
            message += f"{perm}级"
            return message
    return "该指令仅限群聊中使用"


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

    user_id = args.conv["user"][0]
    user_perm = await query_perm(id=str(user_id))
    perm = int(args.perm[0])
    if (args.user or args.group) and (args.is_group):
        return f"非私聊，只能修改当前群聊权限等级"
    if args.user:
        id = user_id
        if user_perm > perm:
            await set_perm(id=id, perm=perm)
            return f"成功设置用户({id})的权限等级为 {perm} 级"
        return f"您的权限等级({user_perm}级)过低，无法修改他人权限等级为 {perm} 级！"
    elif args.group:
        id = args.conv["group"][0]
        if user_perm > perm:
            await set_perm(id=id, perm=perm, isGroup=True)
            return f"成功设置群({id})的权限等级为 {perm} 级"
        return f"您的权限等级({user_perm}级)过低，无法修改群权限等级为 {perm} 级！"
    else:
        id = args.conv["group"][0]
        if user_perm > perm:
            await set_perm(id=id, perm=perm, isGroup=True)
            return f"成功设置本群权限等级为 {perm} 级"
        return f"您的权限等级({user_perm}级)过低，无法修改本群权限等级为 {perm} 级！"
