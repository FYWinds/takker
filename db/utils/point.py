from typing import Union

from tortoise.query_utils import Q

from db.models.config import UserConfig


class Point:
    @staticmethod
    async def query_points(uid: Union[int, str]) -> int:
        """
        :说明: `query_points`
        > 查询用户的积分

        :参数:
          * `uid: Union[int, str]`: QQ号

        :返回:
          - `int`: 积分
        """
        q = await UserConfig.get_or_none(uid=int(uid))
        if q and q.points:
            return q.points
        else:
            return 0

    @staticmethod
    async def set_points(uid: Union[int, str], points: int) -> None:
        """
        :说明: `set_points`
        > 设置用户积分

        :参数:
          * `uid: Union[int, str]`: QQ号
          * `points: int`: 积分
        """
        await UserConfig.update_or_create(uid=int(uid), defaults={"points": points})

    @staticmethod
    async def add_points(uid: Union[int, str], num: int) -> None:
        """
        :说明: `add_points`
        > 给用户添加积分

        :参数:
          * `uid: Union[int, str]`: QQ号
          * `num: int`: 添加的积分数值
        """
        points = await Point.query_points(uid)
        await Point.set_points(uid, points + num)

    @staticmethod
    async def add_random_points(uid: Union[int, str], end: int) -> int:
        """
        :说明: `add_random_points`
        > 给用户添加随机数量的积分，范围为[1,end]

        :参数:
          * `uid: Union[int, str]`: QQ号
          * `endpoint: int`: 最大积分数值
        """
        import random

        num = random.randint(1, end)
        await Point.add_points(uid, num)
        return num

    @staticmethod
    async def take_points(uid: Union[int, str], num: int) -> bool:
        """
        :说明: `take_points`
        > 用户消耗积分

        :参数:
          * `uid: Union[int, str]`: QQ号
          * `num: int`: 减少的积分数值

        :返回:
          - `bool`: 余额是否足够
        """
        points = await Point.query_points(uid)
        if points < num:
            return False
        else:
            await Point.set_points(uid, points - num)
            return True

    @staticmethod
    async def force_take_points(uid: Union[int, str], num: int):
        """
        :说明: `force_take_points`
        > 强制减少用户的积分

        :参数:
          * `uid: Union[int, str]`: QQ号
          * `num: int`: 减少的积分数值
        """
        points = await Point.query_points(uid)
        await Point.set_points(uid, points - num)
