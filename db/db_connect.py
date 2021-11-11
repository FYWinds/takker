import os
import subprocess

from tortoise import Tortoise
from nonebot.log import logger
from tortoise.exceptions import DBConnectionError

from configs.path_config import DATA_PATH

models: list[str] = [
    "db.models.config",
    "db.models.ban",
    "db.models.bs",
    "db.models.statistic",
    "db.models.wordcloud",
    "db.models.outdated_models",
    "aerich.models",
]

TORTOISE_ORM: dict = {
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
            "models": models,
            "default_connection": "data",
        },
        "illustdb": {
            "models": ["db.models.illust"],
            "default_connection": "illust",
        },
    },
}


async def connect_database():
    logger.debug("开始连接数据库")
    try:
        await Tortoise.init(TORTOISE_ORM)
        await Tortoise.generate_schemas()
        logger.info("数据库连接成功")
    except DBConnectionError as e:
        logger.warning("数据库连接失败，请尝试删除data目录下的data.db文件")
        raise e


async def db_disconnect():
    await Tortoise.close_connections()
