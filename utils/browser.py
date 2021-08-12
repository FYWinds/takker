"""
Author: FYWindIsland
Date: 2021-08-10 20:51:15
LastEditTime: 2021-08-11 17:20:36
LastEditors: FYWindIsland
Description: 
I'm writing SHIT codes
"""
import base64
import shutil
from pathlib import Path
from typing import Optional

from appdirs import AppDirs
from nonebot import get_driver
from nonebot.log import logger
from playwright.async_api import Browser, async_playwright


_browser: Optional[Browser] = None


async def init(**kwargs) -> Browser:
    global _browser
    browser = await async_playwright().start()
    _browser = await browser.chromium.launch(**kwargs)
    return _browser


async def get_browser(**kwargs) -> Browser:
    return _browser or await init(**kwargs)
