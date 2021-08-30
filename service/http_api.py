# import httpx

# from configs.config import CQ_HTTP_URL, USE_HTTP_API
# from nonebot.log import logger
from nonebot import get_bot


async def api_get(api: str, **kwargs) -> dict:
    """
    :说明: `api_get`
    > 请求指定的GOCQ API

    :参数:
      * `api: str`: API入口

    :返回:
      - `dict`: 请求返回数据
    """
    # if USE_HTTP_API:
    #     url = f"{CQ_HTTP_URL}/{api}?"
    #     for key, value in kwargs.items():
    #         url += f"{key}={value}&"
    #     data = httpx.get(url).json()
    #     logger.debug(f"CQHTTP | Calling API {api}")
    #     try:
    #         return data["data"]
    #     except KeyError:
    #         return data
    data = await get_bot().call_api(api=api, **kwargs)
    return data
