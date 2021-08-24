"""
Author: FYWindIsland
Date: 2021-08-02 18:57:39
LastEditTime: 2021-08-24 11:04:16
LastEditors: FYWindIsland
Description: 
I'm writing SHIT codes
"""
import random

from nonebot.adapters.cqhttp import Bot, MessageEvent
from nonebot.adapters.cqhttp import Bot, GroupMessageEvent
from nonebot.plugin import get_loaded_plugins, on_command
from nonebot.typing import T_State
from nonebot.exception import NoLogException
from nonebot.log import logger

from api.group_manage import kick
from utils.text_util import cut_text
from utils.data import fortune
from service.db.utils.plugin_manager import set_plugin_status
from configs.path_config import TEMPLATE_PATH

testtest = on_command("test", priority=1, block=True)

__permission__ = 10


@testtest.handle()
async def handle_test(bot: Bot, event: MessageEvent, state: T_State):
    print(event.message)
