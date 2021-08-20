"""
Author: FYWindIsland
Date: 2021-08-14 11:31:43
LastEditTime: 2021-08-20 17:13:37
LastEditors: FYWindIsland
Description: 
I'm writing SHIT codes
"""
from argparse import Namespace

from service.db.utils.statistic import set_illust_status

from .data_source import get_illust


async def handle_get(args: Namespace):
    if args.keywords:
        keyword = args.keywords[0]
    else:
        keyword = ""
    if args.group:
        await set_illust_status(args.group, keyword)
    nsfw_level = 0
    if args.level:
        if args.level[0] in [0, 1, 2]:
            nsfw_level = args.level[0]
        else:
            nsfw_level = 0
    else:
        nsfw_level = 0
    result = await get_illust(nsfw_level, keyword)
    return result
