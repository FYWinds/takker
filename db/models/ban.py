import time

from tortoise.fields import IntField, BigIntField
from tortoise.models import Model
from tortoise.query_utils import Q


class Ban(Model):
    """封禁系统"""

    uid = BigIntField(pk=True)
    ban_level = IntField()
    ban_time = BigIntField()
    duration = BigIntField()

    class Meta:
        table = "ban"
        table_description = "封禁系统数据"
        indexes = ("uid",)

    @classmethod
    async def check_ban(cls, uid: int, ban_level: int = 0) -> bool:
        """
        :说明: `check_ban`
        > 检查用户封禁状态

        :参数:
        * `uid: int`: QQ号
        * `ban_level: int = 0`: 封禁等级，默认为0级

        :返回:
        - `bool`: 封禁状态
        """
        query = await cls.get_or_none(uid=uid)
        if query:
            return query.ban_level >= ban_level
        return False

    @classmethod
    async def get_ban_time(cls, uid: int) -> str:
        """
        :说明: `get_ban_time`
        > 获取用户封禁剩余时间

        :参数:
        * `uid: int`: QQ号

        :返回:
        - `str`: 剩余时间
        """
        query = await cls.get_or_none(uid=uid)
        if query and query.ban_time and query.ban_level:
            ban_time = query.ban_time
            duration = query.duration
        else:
            return ""
        if duration == -1:
            return "∞"
        if time.time() - (ban_time + duration) > 0 and duration != -1:
            return ""
        return str(time.time() - (ban_time + duration))

    @classmethod
    async def isbanned(cls, uid: int) -> bool:
        """
        :说明: `isbanned`
        > 检查用户封禁是否到期

        :参数:
        * `uid: int`: QQ号

        :返回:
        - `bool`: 是否到期
        """
        if await cls.get_ban_time(uid):
            return True
        else:
            await cls.unban(uid)
            return False

    @classmethod
    async def ban(cls, uid: int, ban_level: int, duration: int) -> bool:
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
        query = await cls.get_or_none(uid=uid)
        if query:
            if not cls.check_ban(uid, ban_level):
                await cls.unban(uid)
                await cls.filter(Q(uid=uid)).update(
                    ban_level=ban_level, ban_time=time.time(), duration=duration
                )
                return True
            else:
                return False
        await cls.create(
            uid=uid, ban_level=ban_level, ban_time=time.time(), duration=duration
        )
        return True

    @classmethod
    async def unban(cls, uid: int) -> bool:
        """
        :说明: `unban`
        > 解封用户

        :参数:
        * `uid: int`: QQ号

        :返回:
        - `bool`: 是否解封成功
        """
        query = await cls.filter(Q(uid=uid)).values()
        if query:
            await cls.filter(Q(uid=uid)).delete()
            return True
        else:
            return False
