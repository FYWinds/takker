from tortoise.query_utils import Q

from service.db.model.models import Point


async def query_points(uid: int) -> int:
    """
    :说明: `query_points`
    > 查询用户的积分

    :参数:
      * `uid: int`: QQ号

    :返回:
      - `int`: 积分
    """
    q = await Point.filter(Q(uid=uid)).values()
    if q:
        return q[0]["points"]
    else:
        return 0


async def set_points(uid: int, points: int) -> None:
    """
    :说明: `set_points`
    > 设置用户积分

    :参数:
      * `uid: int`: QQ号
      * `points: int`: 积分
    """
    query = Point.filter(Q(uid=uid))
    if await query.values("points"):
        await query.update(points=points)
    else:
        await Point.create(uid=uid, points=points)


async def add_points(uid: int, num: int) -> None:
    """
    :说明: `add_points`
    > 给用户添加积分

    :参数:
      * `uid: int`: QQ号
      * `num: int`: 添加的积分数值
    """
    points = await query_points(uid)
    await set_points(uid, points + num)


async def add_random_points(uid: int, endpoint: int) -> int:
    """
    :说明: `add_random_points`
    > 给用户添加随机数量的积分，范围为[1,endpoint]

    :参数:
      * `uid: int`: QQ号
      * `endpoint: int`: 最大积分数值
    """
    import random

    num = random.randint(1, endpoint)
    await add_points(uid, num)
    return num


async def take_points(uid: int, num: int) -> bool:
    """
    :说明: `take_points`
    > 用户消耗积分

    :参数:
      * `uid: int`: QQ号
      * `num: int`: 减少的积分数值

    :返回:
      - `bool`: 余额是否足够
    """
    points = await query_points(uid)
    if points < num:
        return False
    else:
        await set_points(uid, points - num)
        return True


async def force_take_points(uid: int, num: int):
    """
    :说明: `force_take_points`
    > 强制减少用户的积分

    :参数:
      * `uid: int`: QQ号
      * `num: int`: 减少的积分数值
    """
    points = await query_points(uid)
    await set_points(uid, points - num)
