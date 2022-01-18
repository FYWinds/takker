import base64
from io import BytesIO
from typing import Union, Literal, Optional
from pathlib import Path

from nonebot.adapters.cqhttp.event import Anonymous

from ._api import BaseAPI


class GroupManagementAPI(BaseAPI):
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

    async def set_group_admin(
        self, group_id: Union[int, str], user_id: Union[int, str], enable: bool
    ) -> None:
        """
        :说明: `set_group_admin`
        > [**群组设置管理员**](https://docs.go-cqhttp.org/api/#%E7%BE%A4%E7%BB%84%E8%AE%BE%E7%BD%AE%E7%AE%A1%E7%90%86%E5%91%98)

        :参数:
          * `group_id: Union[int, str]`: 群号
          * `user_id: Union[int, str]`: 被设置管理员的QQ号
          * `enable: bool`: 是否设置为管理员
        """
        await self.call(
            "set_group_admin", group_id=group_id, user_id=user_id, enable=enable
        )

    async def set_group_card(
        self, group_id: Union[int, str], user_id: Union[int, str], card: str
    ) -> None:
        """
        :说明: `set_group_card`
        > [**设置群名片 ( 群备注 )**](https://docs.go-cqhttp.org/api/#%E8%AE%BE%E7%BD%AE%E7%BE%A4%E5%90%8D%E7%89%87-%E7%BE%A4%E5%A4%87%E6%B3%A8)

        :参数:
          * `group_id: Union[int, str]`: 群号
          * `user_id: Union[int, str]`: 被设置群名片的QQ号
          * `card: str`: 群名片
        """
        await self.call("set_group_card", group_id=group_id, user_id=user_id, card=card)

    async def set_group_name(self, group_id: Union[int, str], group_name: str) -> None:
        """
        :说明: `set_group_name`
        > [**设置群名**](https://docs.go-cqhttp.org/api/#%E8%AE%BE%E7%BD%AE%E7%BE%A4%E5%90%8D)

        :参数:
          * `group_id: Union[int, str]`: 群号
          * `group_name: str`: 群名
        """
        await self.call("set_group_name", group_id=group_id, group_name=group_name)

    async def set_group_leave(self, group_id: Union[int, str], is_dismiss: bool) -> None:
        """
        :说明: `set_group_leave`
        > [**退出群组**](https://docs.go-cqhttp.org/api/#%E9%80%80%E5%87%BA%E7%BE%A4%E7%BB%84)

        :参数:
          * `group_id: Union[int, str]`: 群号
          * `is_dismiss: bool`: 是否解散群组
        """
        await self.call("set_group_leave", group_id=group_id, is_dismiss=is_dismiss)

    async def set_group_special_title(
        self,
        group_id: Union[int, str],
        user_id: Union[int, str],
        special_title: Union[int, str],
        duration: int = -1,
    ) -> None:
        """
        :说明: `set_group_special_title`
        > [**设置群组专属头衔**](https://docs.go-cqhttp.org/api/#%E8%AE%BE%E7%BD%AE%E7%BE%A4%E7%BB%84%E4%B8%93%E5%B1%9E%E5%A4%B4%E8%A1%94)

        :参数:
          * `group_id: Union[int, str]`: 群号
          * `user_id: Union[int, str]`: 被设置专属头衔的QQ号
          * `special_title: Union[int, str]`: 专属头衔

        :可选参数:
          * `duration: int = -1`: 专属头衔持续时间，单位秒，默认为-1，永久
        """
        await self.call(
            "set_group_special_title",
            group_id=group_id,
            user_id=user_id,
            special_title=special_title,
            duration=duration,
        )

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

    async def set_group_add_request(
        self,
        flag: str,
        sub_type: Literal["add", "invite"],
        approve: bool,
        reason: Optional[str] = None,
    ) -> None:
        """
        :说明: `set_group_add_request`
        > [**处理加群请求／邀请**](https://docs.go-cqhttp.org/api/#%E5%A4%84%E7%90%86%E5%8A%A0%E7%BE%A4%E8%AF%B7%E6%B1%82-%E9%82%80%E8%AF%B7)

        :参数:
          * `flag: str`: 加群请求的 flag（需从上报的数据中获得）
          * `sub_type: Literal["add", "invite"]`: add 或 invite, 请求类型（需要和上报消息中的 sub_type 字段相符）
          * `approve: bool`: 是否同意请求／邀请

        :可选参数:
          * `reason: Optional[str] = None`: 拒绝理由（仅在拒绝时有效）
        """
        await self.call(
            "set_group_add_request",
            flag=flag,
            sub_type=sub_type,
            approve=approve,
            reason=reason,
        )

    async def upload_group_file(
        self, group_id: Union[int, str], file: Union[str, Path], name: str, folder: str
    ) -> None:
        """
        :说明: `upload_group_file`
        > [**上传群文件**](https://docs.go-cqhttp.org/api/#%E4%B8%8A%E4%BC%A0%E7%BE%A4%E6%96%87%E4%BB%B6)

        :参数:
          * `group_id: Union[int, str]`: 群号
          * `file: Union[str, Path]`: 文件路径
          * `name: str`: 文件名
          * `folder: str`: 群文件父文件夹 ID
        """
        if isinstance(file, Path):
            file = str(file.resolve())
        await self.call(
            "upload_group_file", group_id=group_id, file=file, name=name, folder=folder
        )

    async def send_group_notice(self, group_id: Union[int, str], content: str) -> None:
        """
        :说明: `send_group_notice`
        > [**发送群公告**](https://docs.go-cqhttp.org/api/#%E5%8F%91%E9%80%81%E7%BE%A4%E5%85%AC%E5%91%8A)

        :参数:
          * `group_id: Union[int, str]`: 群号
          * `content: str`: 公告内容
        """
        await self.call("_send_group_notice", group_id=group_id, content=content)
