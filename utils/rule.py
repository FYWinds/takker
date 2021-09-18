from typing import Union, Optional

from nonebot.log import logger
from nonebot.rule import Rule
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
from nonebot.adapters.cqhttp import MessageEvent, GroupMessageEvent, PrivateMessageEvent
from nonebot.adapters.cqhttp.event import (
    NotifyEvent,
    MessageEvent,
    GroupMessageEvent,
    GroupRequestEvent,
    FriendRequestEvent,
    GroupBanNoticeEvent,
    PrivateMessageEvent,
    FriendAddNoticeEvent,
    GroupAdminNoticeEvent,
    GroupRecallNoticeEvent,
    GroupUploadNoticeEvent,
    FriendRecallNoticeEvent,
    GroupDecreaseNoticeEvent,
    GroupIncreaseNoticeEvent,
)

from configs.config import OWNER, SUPERUSERS


def admin(isGlobal: Optional[bool] = False) -> Rule:
    """
    :说明: `admin`
    > 判断是否是管理触发

    :可选参数:
      * `isGlobal: Optional[bool] = False`: 是否要求全局管理员才可触发，默认否，即群管也可触发
    """

    async def _admin(bot: "Bot", event: "Event", state: T_State) -> bool:
        if not isinstance(event, MessageEvent):
            return False
        _isBotAdmin = str(event.user_id) in SUPERUSERS or str(event.user_id) == OWNER
        if isinstance(event, PrivateMessageEvent):
            return _isBotAdmin
        if isinstance(event, GroupMessageEvent):
            _isGroupAdmin = event.sender.role in ["admin", "owner"]
            if isGlobal:
                return _isBotAdmin
            else:
                return _isBotAdmin or _isGroupAdmin
        return False

    return Rule(_admin)


def limit_group(group_list: list[str]) -> Rule:
    """
    :说明: `limit_group`
    > 限制命令只对指定群组列表和超级用户触发

    :参数:
      * `group: list[str]`: 群号列表
    """

    async def _limit_group(bot: "Bot", event: "Event", state: T_State) -> bool:
        if isinstance(
            event,
            (
                PrivateMessageEvent,
                FriendRequestEvent,
                FriendAddNoticeEvent,
                FriendRecallNoticeEvent,
            ),
        ):
            return str(event.user_id) in SUPERUSERS or str(event.user_id) == OWNER
        if isinstance(
            event,
            (
                GroupMessageEvent,
                GroupRequestEvent,
                GroupAdminNoticeEvent,
                GroupBanNoticeEvent,
                GroupDecreaseNoticeEvent,
                GroupIncreaseNoticeEvent,
                GroupRecallNoticeEvent,
                GroupUploadNoticeEvent,
                NotifyEvent,
            ),
        ):
            _inGroup = str(event.group_id) in group_list
            return _inGroup
        return False

    return Rule(_limit_group)
