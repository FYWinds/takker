"""
Author: FYWindIsland
Date: 2021-08-01 07:48:47
LastEditTime: 2021-08-15 12:00:06
LastEditors: FYWindIsland
Description: 
I'm writing SHIT codes
"""
from configs.path_config import DATA_PATH
from tortoise import Tortoise
import sqlite3

from nonebot.log import logger


async def db_init():
    logger.debug("开始连接数据库")
    try:
        await Tortoise.init(
            {
                "connections": {
                    "data": {
                        "engine": "tortoise.backends.sqlite",
                        "credentials": {"file_path": f"{DATA_PATH}data.db"},
                    },
                    "illust": {
                        "engine": "tortoise.backends.sqlite",
                        "credentials": {"file_path": f"{DATA_PATH}illust.db"},
                    },
                },
                "apps": {
                    "datadb": {
                        "models": ["service.db.model.models"],
                        "default_connection": "data",
                    },
                    "illustdb": {
                        "models": ["service.db.model.illust_model"],
                        "default_connection": "illust",
                    },
                },
            }
        )
        # await Tortoise.init(
        #     db_url=f"sqlite://{DATA_PATH}data.db",
        #     modules={"models": ["service.db.model.models"]},
        # )
        # await Tortoise.generate_schemas()
        # await Tortoise.init(
        #     db_url=f"sqlite://{DATA_PATH}illust.db",
        #     modules={"models": ["service.db.model.illust_model"]},
        # )
        await Tortoise.generate_schemas()
        logger.info("数据库连接成功")
    except:
        logger.warning("数据库连接失败，请尝试删除data目录下的data.db文件")


async def db_disconnect():
    await Tortoise.close_connections()
