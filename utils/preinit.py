import asyncio
import platform
import subprocess

from uvicorn import config
from nonebot.log import logger
from uvicorn.loops import asyncio as _asyncio


def asyncio_setup():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)


@property
def should_reload(self):
    return False


# monkey patch for uvicorn reload bug on windows platform
if platform.system() == "Windows":
    _asyncio.asyncio_setup = asyncio_setup
    config.Config.should_reload = should_reload  # type: ignore
    logger.info("检测到系统为Windows系统，自动注入猴子补丁")
else:
    config.Config.should_reload = should_reload  # type: ignore
    logger.info("已禁用uvicorn自动重载")

# Migration
logger.debug("Migration...")
subprocess.Popen("poetry run aerich upgrade", stdout=subprocess.DEVNULL)
