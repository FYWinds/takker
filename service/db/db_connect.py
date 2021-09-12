from tortoise import Tortoise
from nonebot.log import logger

from configs.path_config import DATA_PATH

models: list[str] = [
    "service.db.models.config",
    "service.db.models.ban",
    "service.db.models.statistic",
    "service.db.models.wordcloud",
    "service.db.models.outdated_models",
]


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
                        "models": [
                            "service.db.models.config",
                            "service.db.models.ban",
                            "service.db.models.statistic",
                            "service.db.models.wordcloud",
                            "service.db.models.outdated_models",
                        ],
                        "default_connection": "data",
                    },
                    "illustdb": {
                        "models": ["service.db.models.illust"],
                        "default_connection": "illust",
                    },
                },
            }
        )
        await Tortoise.generate_schemas()
        logger.info("数据库连接成功")
    except:
        logger.warning("数据库连接失败，请尝试删除data目录下的data.db文件")


async def db_disconnect():
    await Tortoise.close_connections()
