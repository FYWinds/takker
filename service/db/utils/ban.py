import time
from typing import Optional
from tortoise.query_utils import Q

from service.db.model.models import Ban


async def check_ban(uid: int, ban_level: Optional[int] = 0) -> bool:
    """
    :说明: `check_ban`
    > 检查用户封禁状态

    :参数:
      * `uid: int`: QQ号

    :可选参数:
      * `ban_level: Optional[int] = 0`: 封禁等级，默认为0级

    :返回:
      - `bool`: 封禁状态
    """
    query = await Ban.filter(Q(uid=uid)).values()
    if not query:
        return False
    return query[0]["ban_level"] >= ban_level


async def get_ban_time(uid: int) -> str:
    """
    :说明: `get_ban_time`
    > 获取用户封禁剩余时间

    :参数:
      * `uid: int`: QQ号

    :返回:
      - `str`: 剩余时间
    """
    query = await Ban.filter(Q(uid=uid)).values()
    if not query:
        return ""
    ban_time = query[0]["ban_time"]
    duration = query[0]["duration"]
    if time.time() - (ban_time + duration) > 0 and duration != -1:
        return ""
    if duration == -1:
        return "∞"
    return time.time() - (ban_time + duration)


async def isbanned(uid: int) -> bool:
    """
    :说明: `isbanned`
    > 检查用户封禁是否到期

    :参数:
      * `uid: int`: QQ号

    :返回:
      - `bool`: 是否到期
    """
    if await get_ban_time(uid):
        return True
    else:
        await unban(uid)
        return False


async def ban(uid: int, ban_level: int, duration: int) -> bool:
    """
    :说明: `ban`
    > 封禁用户

    :参数:
      * `uid: int`: QQ号
      * `ban_level: int`: 封禁等级
      * `duration: int`: 封禁时间，单位秒

    :返回:
      - `bool`: 是否成功封禁
    """
    query = await Ban.filter(Q(uid=uid)).values()
    if query:
        if not check_ban(uid, ban_level):
            await unban(uid)
            await Ban.filter(Q(uid=uid)).update(
                ban_level=ban_level, ban_time=time.time(), duration=duration
            )
            return True
        else:
            return False
    await Ban.create(
        uid=uid, ban_level=ban_level, ban_time=time.time(), duration=duration
    )
    return True


async def unban(uid: int) -> bool:
    """
    :说明: `unban`
    > 解封用户

    :参数:
      * `uid: int`: QQ号

    :返回:
      - `bool`: 是否解封成功
    """
    query = await Ban.filter(Q(uid=uid)).values()
    if query:
        await Ban.filter(Q(uid=uid)).delete()
        return True
    else:
        return False
