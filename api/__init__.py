from typing import Any, Union, Optional

import nonebot
from nonebot.log import logger
from nonebot.exception import NetworkError
from nonebot.adapters.cqhttp import Message, ActionFailed, escape

from .info import InfoAPI
from .message import MessageAPI
from .group_manage import GroupManagementAPI

__all__ = ["API"]


class BaseAPI:
    async def __init__(self, bot_id: Optional[Union[int, str]]) -> None:
        if bot_id:
            self.bot_id = str(bot_id) if isinstance(bot_id, int) else bot_id

    async def call(self, api: str, **kwargs: Any) -> dict[Any, Any]:
        if self.bot is None:
            try:
                if self.bot_id:
                    self.bot = nonebot.get_bot(self.bot_id)
                else:
                    self.bot = nonebot.get_bot()
            except (ValueError, KeyError) as e:
                logger.error("请求API失败，未连接Bot")
                raise e
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
        except ValueError as e:
            logger.error("请求API失败，未连接Bot")
            raise e


class API(GroupManagementAPI, InfoAPI, MessageAPI):
    async def __init__(self, bot_id: Optional[Union[int, str]]) -> None:
        await super().__init__(bot_id)
