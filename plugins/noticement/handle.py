import random
from asyncio import sleep
from argparse import Namespace

from api.message import send_group_msg, send_private_msg
from configs.config import OWNER

notice: dict[int, dict[int, list[str]]] = {}
# [uid, [gid, noticements[]]]


async def handle_ls(args: Namespace):
    global notice
    if not args.owner:
        message = "您在本次运行中发送过的公告列表: "
    else:
        message = "本次运行中发送过的公告列表: "
    if notice:
        for g in notice[args.user]:
            message += f"\n{g}: {notice[args.user][g]}"
        return message
    else:
        return "您在本次运行中未曾发送过公告"


async def handle_send(args: Namespace):
    global notice
    groups = args.groups
    if args.notice:
        this_notice = "\n".join(args.notice)
        this_notice = f"=-=-=-=-公告-=-=-=-=\n{this_notice}\n=-=-=-=-=-=-=-=-=-="
    else:
        return "请输入要发送的公告内容"
    if groups:
        for g in groups:
            await send_group_msg(g, this_notice)
            sleep_time = random.random() + 1
            await sleep(sleep_time)
            history_notice = args.notice
            if notice:
                if args.user in notice:
                    if g in notice[args.user]:
                        history_notice = notice[args.user][g]
                        history_notice += args.notice
            if args.user in notice:
                notice[args.user] |= {g: history_notice}
            else:
                notice |= {args.user: {g: history_notice}}
            if args.user not in OWNER:
                await send_private_msg(
                    uid=int(OWNER),
                    message=f"超级管理员({args.user})向群{args.groups}发送了公告，内容为: {args.notice[0]}",
                )
    return "公告发送成功"
