"""
Author: FYWindIsland
Date: 2021-08-10 20:20:38
LastEditTime: 2021-08-12 13:01:23
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


def patch():
    if platform.system() == "Windows":
        _asyncio.asyncio_setup = asyncio_setup()
        config.Config.should_reload = False  # type: ignore
        logger.info("检测到当前为 Windows 系统，已自动注入猴子补丁")
