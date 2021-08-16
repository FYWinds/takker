"""
Author: FYWindIsland
Date: 2021-08-15 08:43:51
LastEditTime: 2021-08-15 09:16:13
LastEditors: FYWindIsland
Description: Not Finished, lacking ideas
I'm writing SHIT codes
"""
from typing import Optional

from nonebot.adapters import Bot
from nonebot.message import run_postprocessor
from nonebot.matcher import Matcher
from nonebot.adapters import Event
from nonebot.typing import T_State


@run_postprocessor
async def log_msg(
    matcher: Matcher,
    exception: Optional[Exception],
    bot: Bot,
    event: Event,
    state: T_State,
):
    pass
