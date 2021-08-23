"""
Author: FYWindIsland
Date: 2021-08-14 11:31:43
LastEditTime: 2021-08-23 18:03:47
LastEditors: FYWindIsland
Description: 
I'm writing SHIT codes
"""
from argparse import Namespace

from service.db.utils.statistic import set_illust_status

from .data_source import get_illust, get_illust_direct


async def handle_get(args: Namespace):
    if args.keywords:
        keywords = args.keywords
    else:
        keywords = []
    if len(keywords) == 1 and keywords[0].isdigit():
        try:
            result = await get_illust_direct(keywords[0])
            return result
        except:
            pass
    if args.group:
        await set_illust_status(args.group, keywords)
    nsfw_level = 0
    if args.level:
        if args.level[0] in [0, 1, 2]:
            nsfw_level = args.level[0]
        else:
            nsfw_level = 0
    else:
        nsfw_level = 0
    result = await get_illust(nsfw_level, keywords)
    return result
