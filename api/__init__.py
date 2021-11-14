from typing import Any

import nonebot
from nonebot.log import logger
from nonebot.exception import NetworkError
from nonebot.adapters.cqhttp import Message, ActionFailed, escape

from .info import InfoAPI
from .message import MessageAPI
from .group_manage import GroupManagementAPI

InfoAPI = InfoAPI()
MessageAPI = MessageAPI()
GroupManagementAPI = GroupManagementAPI()

__all__ = ["InfoAPI", "MessageAPI", "GroupManagementAPI"]


class API:
    def __init__(self):
        try:
            self.bot = nonebot.get_bot()
        except ValueError:
            self.bot = None

    async def call(self, api: str, **kwargs: Any) -> dict[Any, Any]:
        if self.bot is None:
            try:
                self.bot = nonebot.get_bot()
            except ValueError:
                logger.error("请求API失败，未连接Bot")
                raise NetworkError("请求API失败，未连接Bot")
        try:
            try:
                if "user_id" in kwargs:
                    kwargs["user_id"] = int(kwargs["user_id"])
                if "group_id" in kwargs:
                    kwargs["group_id"] = int(kwargs["group_id"])
                if "message_id" in kwargs:
                    kwargs["message_id"] = (
                        int(kwargs["message_id"])
                        if kwargs["message_id"].isdigit()
                        else kwargs["message_id"]
                    )
                if "message" in kwargs:
                    message = kwargs["message"]
                    message = (
                        escape(message, escape_comma=False)
                        if isinstance(message, str)
                        else message
                    )
                    message = (
                        message if isinstance(message, Message) else Message(message)
                    )
            except ValueError:
                raise TypeError("请求API参数类型错误")
            data: dict[Any, Any] = await self.bot.call_api(api, **kwargs)
            if data.get("retcode") == 100 or data.get("status") == "failed":
                raise ActionFailed(**data)
            return data
        except ValueError:
            logger.error("请求API失败，未连接Bot")
            raise NetworkError("请求API失败，未连接Bot")
