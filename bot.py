"""
Author: FYWindIsland
Date: 2021-08-01 07:48:44
LastEditTime: 2021-08-24 18:26:17
LastEditors: FYWindIsland
Description: 
I'm writing SHIT codes
"""
import nonebot
from nonebot.adapters.cqhttp import Bot as CQHTTPBot

from service.db.database_sqlite import db_disconnect
from service.init import init_bot
from utils.patcher import patch


nonebot.init()
driver = nonebot.get_driver()
driver.register_adapter("cqhttp", CQHTTPBot)
config = driver.config

patch()

driver.on_startup(init_bot)
driver.on_shutdown(db_disconnect)


nonebot.load_plugins("plugins")
nonebot.load_from_toml("pyproject.toml")


app = nonebot.get_asgi()

if __name__ == "__main__":
    nonebot.run(app="__mp_main__:app")
