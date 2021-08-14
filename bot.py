"""
Author: FYWindIsland
Date: 2021-08-01 07:48:44
LastEditTime: 2021-08-13 13:49:52
LastEditors: FYWindIsland
Description: 
I'm writing SHIT codes
"""
import nonebot
from nonebot.adapters.cqhttp import Bot as CQHTTPBot

from service.db.database_sqlite import db_disconnect
from service.init import init_bot


nonebot.init()
driver = nonebot.get_driver()
driver.register_adapter("cqhttp", CQHTTPBot)
config = driver.config


driver.on_startup(init_bot)
driver.on_shutdown(db_disconnect)

# nonebot.load_builtin_plugins()
nonebot.load_plugins("plugins")
nonebot.load_from_toml("pyproject.toml")


app = nonebot.get_asgi()

if __name__ == "__main__":
    nonebot.run(app="__mp_main__:app")
