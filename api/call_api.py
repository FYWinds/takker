from typing import Any

from nonebot import get_bot
from nonebot.log import logger


async def call(api: str, **kwargs: Any) -> dict[Any, Any]:
    """
    :说明: `call`
    > 请求指定的GOCQ API

    :参数:
      * `api: str`: API入口

    :返回:
      - `dict`: 请求返回数据
    """
    try:
        data: dict[Any, Any] = await get_bot().call_api(api=api, **kwargs)
        return data
    except ValueError as e:
        logger.error("请求API失败，未连接Bot")
        raise e
