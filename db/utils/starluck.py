from typing import Union

from db.models.config import UserConfig


class Starluck:
    @staticmethod
    async def query_star(uid: Union[int, str]) -> int:
        """
        :说明: `query_star`
        > 查询用户的绑定星座

        :参数:
          * `uid: Union[int, str]`: QQ号

        :返回:
          - `int`: 星座ID
        """
        p = await UserConfig.get_or_none(uid=int(uid))
        if p and p.constellation:
            return p.constellation
        return 0

    @staticmethod
    async def set_star(uid: Union[int, str], constellation: int) -> None:
        """
        :说明: `set_user_star`
        > 绑定用户星座

        :参数:
          * `uid: Union[int, str]`: QQ号
          * `star: int`: 星座ID
        """
        await UserConfig.update_or_create(
            uid=int(uid), defaults={"constellation": constellation}
        )
