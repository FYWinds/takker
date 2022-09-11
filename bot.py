"""
Author       : FYWinds i@windis.cn
Date         : 2021-08-16 22:22:52
LastEditors  : FYWinds i@windis.cn
LastEditTime : 2022-09-07 02:55:38
FilePath     : /bot.py

Copyright (c) 2022 by FYWinds i@windis.cn
All Rights Reserved.
Any modifications or distributions of the file
should mark the original author's name.
"""

import sys

import nonebot
from nonebot.adapters.onebot.v11 import Adapter as OneBotV11Adapter

from utils.init import init_bot_startup, update_plugin_list
from db.db_connect import db_disconnect
from utils.browser import close_browser

if __name__ != "__main__":
    print("You should directly run this file!")
    print("Exiting...")
    sys.exit(1)

env_file: str = f".env.{sys.argv[1]}" if len(sys.argv) > 1 else ".env.prod"
nonebot.init(_env_file=env_file)

driver = nonebot.get_driver()
driver.register_adapter(OneBotV11Adapter)

update_plugin_list(driver)

driver.on_startup(init_bot_startup)
driver.on_shutdown(db_disconnect)
driver.on_shutdown(close_browser)

# load the apscheduler at the first place
nonebot.load_plugin("nonebot_plugin_apscheduler")
nonebot.load_plugins("plugins")

app = nonebot.get_asgi()
nonebot.run(app="__mp_main__:app")
