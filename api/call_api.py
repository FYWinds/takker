from nonebot import get_bot


async def call(api: str, **kwargs) -> dict:
    """
    :说明: `call`
    > 请求指定的GOCQ API

    :参数:
      * `api: str`: API入口

    :返回:
      - `dict`: 请求返回数据
    """
    data = await get_bot().call_api(api=api, **kwargs)
    return data
