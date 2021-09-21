from typing import Union, Optional

from nonebot.rule import Rule
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event

from configs.config import OWNER, SUPERUSERS


def admin(isGlobal: Optional[bool] = False) -> Rule:
    """
    :说明: `admin`
    > 判断是否是管理触发

    :可选参数:
      * `isGlobal: Optional[bool] = False`: 是否要求全局管理员才可触发，默认否，即群管也可触发
    """

    async def _admin(bot: "Bot", event: "Event", state: T_State) -> bool:
        user_id = getattr(event, "user_id", None)
        group_id = getattr(event, "group_id", None)
        role = getattr(getattr(event, "sender", None), "role", None)
        # 不包含用户/群的事件不做响应
        if user_id == None and group_id == None:
            return False
        _isBotAdmin = str(user_id) in SUPERUSERS or str(user_id) == OWNER

        if role is not None:
            _isGroupAdmin = role in ["admin", "owner"]
            if isGlobal:
                return _isBotAdmin
            else:
                return _isBotAdmin or _isGroupAdmin

        if user_id is not None and group_id == None:
            return _isBotAdmin

        return False

    return Rule(_admin)


def limit_group(group_list: list[Union[int, str]]) -> Rule:
    """
    :说明: `limit_group`
    > 限制命令只对指定群组列表和超级用户触发

    :参数:
      * `group: list[str | int]`: 群号列表
    """
    group_list = list(map(str, group_list))

    async def _limit_group(bot: "Bot", event: "Event", state: T_State) -> bool:
        user_id = getattr(event, "user_id", None)
        group_id = getattr(event, "group_id", None)
        if group_id:
            return str(group_id) in group_list
        if user_id:
            return str(user_id) in SUPERUSERS or str(user_id) == OWNER
        return False

    return Rule(_limit_group)
