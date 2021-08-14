"""
Author: FYWindIsland
Date: 2021-08-14 11:31:43
LastEditTime: 2021-08-14 13:33:23
LastEditors: FYWindIsland
Description: 
I'm writing SHIT codes
"""
from argparse import Namespace

from utils.utils import Processing

from .data_source import get_illust

_plmt = Processing()


async def handle_get(args: Namespace):
    _plmt.set_True(args.user)
    print(args.keywords, args.level)
    if args.keywords:
        keyword = args.keywords[0]
    else:
        keyword = ""
    nsfw_level = 0
    if args.level:
        if args.level[0] in [0, 1, 2]:
            nsfw_level = args.level[0]
        else:
            nsfw_level = 0
    else:
        nsfw_level = 0
    result = await get_illust(nsfw_level, keyword)
    _plmt.set_False(args.user)
    return result
