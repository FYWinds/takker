import nonebot
from nonebot.adapters.cqhttp import Bot as CQHTTPBot

import utils.preinit  # type: ignore
from utils.init import init_bot_startup, update_plugin_list
from db.db_connect import db_disconnect
from utils.browser import close_browser
from utils.shutdown import shut_down

nonebot.init()

driver = nonebot.get_driver()
driver.register_adapter("cqhttp", CQHTTPBot)
config = driver.config

update_plugin_list(driver)

driver.on_startup(init_bot_startup)
driver.on_shutdown(db_disconnect)
driver.on_shutdown(close_browser)
driver.on_shutdown(shut_down)


nonebot.load_plugins("plugins")
nonebot.load_from_toml("pyproject.toml")


app = nonebot.get_asgi()

if __name__ == "__main__":
    nonebot.run(app="__mp_main__:app")
