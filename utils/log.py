from nonebot.log import logger
from configs.path_config import LOG_PATH

custom_format = (
    "<g>{time:YYYY-MM-DD HH:mm:ss}</g> " "[{level}] " "{name} | " "{message}"
)


async def log_to_file():
    logger.add(
        LOG_PATH + "debug/{time:YYYY-MM-DD}.log",
        rotation="00:00",
        retention="10 days",
        level="DEBUG",
        format=custom_format,
        encoding="utf-8",
    )
    logger.add(
        LOG_PATH + "info/{time:YYYY-MM-DD}.log",
        rotation="00:00",
        retention="3 months",
        level="INFO",
        format=custom_format,
        encoding="utf-8",
    )
    logger.add(
        LOG_PATH + "error/{time:YYYY-MM-DD}.log",
        rotation="00:00",
        retention="1 year",
        level="ERROR",
        format=custom_format,
        encoding="utf-8",
    )
