#!/usr/bin/env python3
# -*- coding: utf-8 -*-
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
