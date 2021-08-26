import nonebot
from nonebot.adapters.cqhttp import Bot as CQHTTPBot

from service.db.database_sqlite import db_disconnect
from service.init import init_bot
from utils.patcher import patch
from utils.browser import close_browser


nonebot.init()
driver = nonebot.get_driver()
driver.register_adapter("cqhttp", CQHTTPBot)
config = driver.config

patch()

driver.on_startup(init_bot)
driver.on_shutdown(db_disconnect)
driver.on_shutdown(close_browser)


nonebot.load_plugins("plugins")
nonebot.load_from_toml("pyproject.toml")


app = nonebot.get_asgi()

if __name__ == "__main__":
    nonebot.run(app="__mp_main__:app")
