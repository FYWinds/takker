import base64
from io import BytesIO
from typing import Union, Optional
from pathlib import Path

from nonebot.adapters.cqhttp.event import Anonymous

from utils.utils import deprecated

from . import API


@deprecated("此API不稳定， 登录一段时间后失效，不建议使用")
async def set_group_portrait(
    self,
    group_id: Union[int, str],
    file: Union[str, Path, bytes, BytesIO],
    cache: int = 1,
) -> None:
    """
    :说明: `set_group_portrait`
    > 设置群头像

    不稳定， 登录一段时间后失效，不建议使用

    :参数:
        * `group_id: Union[int, str]`: 群号
        * `file: Union[str, Path, bytes, BytesIO]`: 图片文件

    :可选参数:
        * `cache: int = 1`: 使用URL图片时，是否使用已缓存的文件

    :异常:
        * `TypeError`: 文件解析错误
    """
    if isinstance(file, BytesIO):
        file = file.getvalue()
    if isinstance(file, bytes):
        file = "base64://" + base64.b64encode(file).decode()
    if isinstance(file, Path):
        file = str(file.resolve())
    if not isinstance(file, str):
        raise TypeError("file must be str, Path , bytes or BytesIO")
    if not file.startswith(("file:///", "base64://", "http://", "https://")):
        file = "file:///" + file
    await self.call("set_group_portrait", group_id=group_id, file=file, cache=cache)


class GroupManagementAPI(API):
    async def set_group_kick(
        self,
        group_id: Union[int, str],
        user_id: Union[int, str],
        reject_add_request: bool = False,
    ) -> None:
        """
        :说明: `set_group_kick`
        > [**群组踢人**](https://docs.go-cqhttp.org/api/#%E7%BE%A4%E7%BB%84%E8%B8%A2%E4%BA%BA)

        :参数:
          * `group_id: Union[int, str]`: 群号
          * `user_id: Union[int, str]`: 被踢人的QQ号

        :可选参数:
          * `reject_add_request: bool = False`: 是否拒绝被踢人再次加群请求
        """
        await self.call(
            "set_group_kick",
            group_id=group_id,
            user_id=user_id,
            reject_add_request=reject_add_request,
        )

    async def set_group_ban(
        self,
        group_id: Union[int, str],
        user_id: Union[int, str],
        duration: Optional[int] = 0,
    ) -> None:
        """
        :说明: `set_group_ban`
        > [**群组单人禁言**](https://docs.go-cqhttp.org/api/#%E7%BE%A4%E7%BB%84%E5%8D%95%E4%BA%BA%E7%A6%81%E8%A8%80)

        :参数:
          * `group_id: Union[int, str]`: 群号
          * `user_id: Union[int, str]`: 被禁言人的QQ号

        :可选参数:
          * `duration: Optional[int] = 0`: 禁言时长，单位为秒，0为解除禁言
        """
        await self.call(
            "set_group_ban", group_id=group_id, user_id=user_id, duration=duration
        )

    async def set_group_anonymous_ban(
        self,
        group_id: Union[int, str],
        anonymous: Optional[Anonymous] = None,
        flag: Optional[str] = None,
        duration: Optional[int] = 0,
    ) -> None:
        """
        :说明: `set_group_anonymous_ban`
        > [**群组匿名用户禁言**](https://docs.go-cqhttp.org/api/#%E7%BE%A4%E7%BB%84%E5%8C%BF%E5%90%8D%E7%94%A8%E6%88%B7%E7%A6%81%E8%A8%80)

        :参数:
          * `group_id: Union[int, str]`: 群号

        :可选参数:
          * `anonymous: Optional[Anonymous] = None`: 匿名用户对象，从上报数据中获得
          * `flag: Optional[str] = None`: 匿名用户的flag，从上报数据中获得
          * `duration: Optional[int] = 0`: 禁言时长，单位为秒，0为解除禁言

        :异常:
          - `TypeError`: `anonymous`或`flag`至少填一个
        """
        if not anonymous and not flag:
            raise TypeError("anonymous or flag must be set")
        await self.call(
            "set_group_anonymous_ban",
            group_id=group_id,
            anonymous=anonymous,
            flag=flag,
            duration=duration,
        )

    async def set_group_whole_ban(self, group_id: Union[int, str], enable: bool) -> None:
        """
        :说明: `set_group_whole_ban`
        > [**群组全员禁言**](https://docs.go-cqhttp.org/api/#%E7%BE%A4%E7%BB%84%E5%85%A8%E5%91%98%E7%A6%81%E8%A8%80)

        :参数:
          * `group_id: Union[int, str]`: 群号
          * `enable: bool`: 是否禁言
        """
        await self.call("set_group_whole_ban", group_id=group_id, enable=enable)
