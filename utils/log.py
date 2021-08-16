"""
Author: FYWindIsland
Date: 2021-08-14 11:47:29
LastEditTime: 2021-08-16 10:09:52
LastEditors: FYWindIsland
Description: 
I'm writing SHIT codes
"""
from nonebot.log import logger, default_format
from configs.path_config import LOG_PATH

custom_format = (
    "<g>{time:YYYY-MM-DD HH:mm:ss}</g> " "[{level}] " "{name} | " "{message}"
)


async def log_to_file():
    logger.add(
        LOG_PATH + "debug/{time:YYYY-MM-DD}.log",
        rotation="00:00",
        retention="15 days",
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
