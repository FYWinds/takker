from typing import List, Union, Optional

from nonebot.adapters.cqhttp import Message, MessageSegment, GroupMessageEvent

from ._api import BaseAPI
from .models import *


class MessageAPI(BaseAPI):
    async def friend_message(
        self, user_id: Union[int, str], message: Union[str, Message, MessageSegment]
    ) -> int:
        """
        :说明: `friend`
        > [**发送私聊消息**](https://docs.go-cqhttp.org/api/#%E5%8F%91%E9%80%81%E7%A7%81%E8%81%8A%E6%B6%88%E6%81%AF)

        :参数:
          * `user_id: Union[int, str]`: QQ号
          * `message: Message`: 消息

        :返回:
          - `int`: 消息ID
        """
        return (await self.call("send_private_msg", user_id=user_id, message=message))[
            "message_id"
        ]

    async def stranger_message(
        self,
        user_id: Union[int, str],
        group_id: Union[int, str],
        message: Union[str, Message, MessageSegment],
    ) -> int:
        """
        :说明: `stranger`
        > 通过群聊向陌生人发送私聊消息， 机器人必须是管理员/群主

        :参数:
          * `user_id: Union[int, str]`: QQ号
          * `group_id: Union[int, str]`: 群号
          * `message: Union[str, Message, MessageSegment]`: 消息

        :返回:
          - `int`: 消息ID
        """
        return (
            await self.call(
                "send_private_msg", user_id=user_id, group_id=group_id, message=message
            )
        )["message_id"]

    async def group_message(
        self, group_id: Union[int, str], message: Union[str, Message, MessageSegment]
    ) -> int:
        """
        :说明: `group`
        > [**发送群聊消息**](https://docs.go-cqhttp.org/api/#%E5%8F%91%E9%80%81%E7%BE%A4%E6%B6%88%E6%81%AF)

        :参数:
          * `group_id: Union[int, str]`: 群号
          * `message: Union[str, Message, MessageSegment]`: 消息

        :返回:
          - `int`: 消息ID
        """
        return (await self.call("send_group_msg", group_id=group_id, message=message))[
            "message_id"
        ]

    async def send_msg(
        self,
        message: Union[str, Message, MessageSegment],
        user_id: Optional[Union[int, str]] = None,
        group_id: Optional[Union[int, str]] = None,
    ) -> int:
        """
        :说明: `send_msg`
        > [**发送消息**](https://docs.go-cqhttp.org/api/#%E5%8F%91%E9%80%81%E6%B6%88%E6%81%AF)

        :参数:
          * `message: Union[str, Message, MessageSegment]`: 消息

        :可选参数:
          * `user_id: Optional[Union[int, str]] = None`: QQ号
          * `group_id: Optional[Union[int, str]] = None`: 群号

        :Exceptions:
          * `ValueError`: user_id 和 group_id 不能同时为空
          * `ValueError`: user_id 和 group_id 不能同时为非空

        :返回:
          - `int`: [description]
        """
        if user_id and group_id:
            raise ValueError("user_id and group_id cannot be provided together")
        if user_id:
            return (await self.call("send_msg", user_id=user_id, message=message))[
                "message_id"
            ]
        elif group_id:
            return (await self.call("send_msg", group_id=group_id, message=message))[
                "message_id"
            ]
        else:
            raise ValueError("user_id or group_id must be provided")

    async def get_group_msg_history(
        self, message_seq: Union[int, str], group_id: Union[int, str]
    ) -> List[Union[GroupMessageEvent, SelfGroupMessage]]:
        """
        :说明: `get_group_msg_history`
        > [**获取群消息历史记录**](https://docs.go-cqhttp.org/api/#%E8%8E%B7%E5%8F%96%E7%BE%A4%E6%B6%88%E6%81%AF%E5%8E%86%E5%8F%B2%E8%AE%B0%E5%BD%95)

        :参数:
          * `message_seq: Union[int, str]`: 起始消息序号, 可通过 get_msg 获得
          * `group_id: Union[int, str]`: 群号

        :返回:
          - `List[Union[GroupMessageEvent, SelfGroupMessage]]`: 从起始序号开始的前19条消息，按照时间顺序正序排列，包含Bot自身发出的消息
        """
        return [
            GroupMessageEvent(**msg)
            if msg["post_type"] == "message"
            else SelfGroupMessage(**msg)
            for msg in await self.call(
                "get_group_msg_history", message_seq=message_seq, group_id=group_id
            )
        ]

    async def get_msg(
        self, message_id: Union[int, str]
    ) -> Union[MessageGot, GroupMessageGot]:
        """
        :说明: `get_msg`
        > [**获取消息**](https://docs.go-cqhttp.org/api/#%E8%8E%B7%E5%8F%96%E6%B6%88%E6%81%AF)

        :参数:
          * `message_id: Union[int, str]`: 消息ID

        :返回:
          - `Union[MessageGot, GroupMessageGot]`: 消息
        """
        msg = await self.call("get_msg", message_id=message_id)
        return (
            GroupMessageGot(**msg)
            if msg["message_type"] == "group"
            else MessageGot(**msg)
        )

    async def delete_msg(self, message_id: Union[int, str]) -> None:
        """
        :说明: `delete_msg`
        > [**撤回消息**](https://docs.go-cqhttp.org/api/#%E6%92%A4%E5%9B%9E%E6%B6%88%E6%81%AF)

        :参数:
          * `message_id: Union[int, str]`: 消息ID
        """
        await self.call("delete_msg", message_id=message_id)

    async def get_forward_msg(self, message_id: str) -> List[ForwardMsg]:
        """
        :说明: `get_forward_msg`
        > [**获取合并转发内容**](https://docs.go-cqhttp.org/api/#%E8%8E%B7%E5%8F%96%E5%90%88%E5%B9%B6%E8%BD%AC%E5%8F%91%E5%86%85%E5%AE%B9)

        :参数:
          * `message_id: str`: 合并转发中的消息ID

        :返回:
          - `List[ForwardMsg]`: 合并转发内容
        """
        return [
            ForwardMsg(**msg)
            for msg in await self.call("get_forward_msg", message_id=message_id)
        ]

    async def send_group_forward_msg(
        self, group_id: Union[int, str], messages: List[Union[str, MessageSegment]]
    ) -> int:
        """
        :说明: `send_group_forward_msg`
        > 发送合并转发(群聊)

        :参数:
          * `group_id: Union[int, str]`: 群号
          * `messages: List[Union[str, MessageSegment]]`: 合并转发节点，建议使用 `MessageSegment.node()` 方法构造

        :返回:
          - `int`: [description]
        """
        return (
            await self.call(
                "send_group_forward_msg", group_id=group_id, messages=messages
            )
        )["message_id"]

    async def set_essence_msg(self, message_id: Union[int, str]) -> None:
        """
        :说明: `set_essence_msg`
        > [**设置精华消息**](https://docs.go-cqhttp.org/api/#%E8%AE%BE%E7%BD%AE%E7%B2%BE%E5%8D%8E%E6%B6%88%E6%81%AF)

        :参数:
          * `message_id: Union[int, str]`: 消息ID
        """
        await self.call("set_essence_msg", message_id=message_id)

    async def delete_essence_msg(self, message_id: Union[int, str]) -> None:
        """
        :说明: `delete_essence_msg`
        > [**移出精华消息**](https://docs.go-cqhttp.org/api/#%E7%A7%BB%E5%87%BA%E7%B2%BE%E5%8D%8E%E6%B6%88%E6%81%AF)

        :参数:
          * `message_id: Union[int, str]`: 消息ID
        """
        await self.call("delete_essence_msg", message_id=message_id)
