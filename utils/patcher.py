"""
Author: FYWindIsland
Date: 2021-08-10 20:20:38
LastEditTime: 2021-08-20 17:59:15
LastEditors: FYWindIsland
Description: 
I'm writing SHIT codes
"""
import asyncio
import platform
from uvicorn.loops import asyncio as _asyncio
from uvicorn import config
from nonebot.log import logger


def asyncio_setup():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)


@property
def should_reload(self):
    return False


def patch():
    if platform.system() == "Windows":
        _asyncio.asyncio_setup = asyncio_setup
        config.Config.should_reload = should_reload  # type: ignore
        logger.info("检测到系统为Windows系统，自动注入猴子补丁")
    else:
        config.Config.should_reload = should_reload  # type: ignore
        logger.info("已禁用uvicorn自动重载")
