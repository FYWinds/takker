from typing import List, Union, Literal

from ._api import BaseAPI
from .models import *


class InfoAPI(BaseAPI):
    async def get_login_info(self) -> BaseUserInfo:
        """
        :说明: `login_info`
        > [**获取登录账号信息**](https://docs.go-cqhttp.org/api/#%E8%8E%B7%E5%8F%96%E7%99%BB%E5%BD%95%E5%8F%B7%E4%BF%A1%E6%81%AF)

        :返回:
          - `BaseUserInfo`: 响应数据 参考GOCQ文档
        """
        return BaseUserInfo(**await self.call("get_login_info"))

    async def get_stranger_info(
        self, user_id: Union[int, str], no_cache: bool = True
    ) -> UserInfo:
        """
        :说明: `stranger_info`
        > [**获取陌生人信息**](https://docs.go-cqhttp.org/api/#%E8%8E%B7%E5%8F%96%E9%99%8C%E7%94%9F%E4%BA%BA%E4%BF%A1%E6%81%AF)

        :参数:
          * `user_id: Union[int, str]`: QQ号

        :可选参数:
          * `no_cache: bool = True`: 是否不使用GOCQ端本地缓存的信息，默认不使用缓存

        :返回:
          - `UserInfo`: 响应数据 参考GOCQ文档
        """
        return UserInfo(
            **await self.call("get_stranger_info", user_id=user_id, no_cache=no_cache)
        )

    async def get_group_info(
        self, group_id: Union[int, str], no_cache: bool = True
    ) -> GroupInfo:
        """
        :说明: `group_info`
        > [**获取群信息**](https://docs.go-cqhttp.org/api/#%E8%8E%B7%E5%8F%96%E7%BE%A4%E4%BF%A1%E6%81%AF)

        :参数:
          * `group_id: Union[int, str]`: 群号

        :可选参数:
          * `no_cache: bool = True`: 是否不使用GOCQ端本地缓存的信息，默认不使用缓存

        :返回:
          - `dict[Any, Any]`: 响应数据 参考GOCQ文档
        """
        return GroupInfo(
            **(await self.call("get_group_info", group_id=group_id, no_cache=no_cache))
        )

    async def get_friend_list(self) -> List[FriendInfo]:
        """
        :说明: `friend_list`
        > [**获取好友列表**](https://docs.go-cqhttp.org/api/#%E8%8E%B7%E5%8F%96%E5%A5%BD%E5%8F%8B%E5%88%97%E8%A1%A8)

        :返回:
          - `dict[Any, Any]`: 响应数据 参考GOCQ文档
        """
        return [FriendInfo(**i) for i in (await self.call("get_friend_list"))]

    async def get_group_list(self) -> List[GroupInfo]:
        """
        :说明: `group_list`
        > [**获取群列表**](https://docs.go-cqhttp.org/api/#%E8%8E%B7%E5%8F%96%E7%BE%A4%E5%88%97%E8%A1%A8)

        :返回:
          - `dict[Any, Any]`: 响应数据 参考GOCQ文档
        """
        return [GroupInfo(**i) for i in (await self.call("get_group_list"))]

    async def get_group_member_info(
        self, group_id: Union[int, str], user_id: Union[int, str]
    ) -> GroupMemberInfo:
        """
        :说明: `group_member_info`
        > [**获取群成员信息**](https://docs.go-cqhttp.org/api/#%E8%8E%B7%E5%8F%96%E7%BE%A4%E6%88%90%E5%91%98%E4%BF%A1%E6%81%AF)

        :参数:
          * `group_id: Union[int, str]`: 群号

        :返回:
          - `dict[Any, Any]`: 响应数据 参考GOCQ文档
        """
        return GroupMemberInfo(
            **(await self.call("get_group_member_info", group_id=group_id))
        )

    async def get_group_member_list(
        self, group_id: Union[int, str]
    ) -> List[GroupMemberInfo]:
        """
        :说明: `group_member_list`
        > [**获取群成员列表**](https://docs.go-cqhttp.org/api/#%E8%8E%B7%E5%8F%96%E7%BE%A4%E6%88%90%E5%91%98%E5%88%97%E8%A1%A8)，返回数据量较获取群成员信息少

        :参数:
          * `group_id: Union[int, str]`: 群号

        :返回:
          - `dict[Any, Any]`: 响应数据 参考GOCQ文档
        """
        return [
            GroupMemberInfo(**i)
            for i in (await self.call("get_group_member_list", group_id=group_id))
        ]

    async def get_group_honor_info(
        self,
        group_id: Union[int, str],
        type: Literal[
            "talkative", "performer", "legend", "strong_newbie", "emotion", "all"
        ] = "all",
    ) -> HonorInfo:
        """
        :说明: `group_honor_info`
        > [**获取群荣誉信息**](https://docs.go-cqhttp.org/api/#%E8%8E%B7%E5%8F%96%E7%BE%A4%E8%8D%A3%E8%AA%89%E4%BF%A1%E6%81%AF)

        :参数:
          * `group_id: Union[int, str]`: 群号

        :可选参数:
          * `type: str = "all"`: 群荣誉类型
          可选`talkative` `performer` `legend` `strong_newbie` `emotion`
          默认获取全部

        :返回:
          - `dict[Any, Any]`: 响应数据 参考GOCQ文档
        """
        return HonorInfo(
            **(
                await self.call(
                    "get_group_honor_info", group_id=group_id, type=str(type)
                )
            )
        )

    async def get_group_system_msg(self) -> GroupSystemMsg:
        """
        :说明: `get_group_system_msg`
        > [**获取群系统消息**](https://docs.go-cqhttp.org/api/#%E8%8E%B7%E5%8F%96%E7%BE%A4%E7%B3%BB%E7%BB%9F%E6%B6%88%E6%81%AF)

        :返回:
          - `GroupSystemMsg`: 加群申请&邀请，字段见GOCQ文档
        """
        return GroupSystemMsg(**(await self.call("get_group_system_msg")))

    async def can_send_image(self) -> bool:
        """
        :说明: `can_send_image`
        > [**检查是否可以发送图片**](https://docs.go-cqhttp.org/api/#%E6%A3%80%E6%9F%A5%E6%98%AF%E5%90%A6%E5%8F%AF%E4%BB%A5%E5%8F%91%E9%80%81%E5%9B%BE%E7%89%87)

        :返回:
          - `bool`: 能否发送图片
        """
        return (await self.call("can_send_image")).get("yes", False)

    async def can_send_record(self) -> bool:
        """
        :说明: `can_send_record`
        > [**检查是否可以发送语音**](https://docs.go-cqhttp.org/api/#%E6%A3%80%E6%9F%A5%E6%98%AF%E5%90%A6%E5%8F%AF%E4%BB%A5%E5%8F%91%E9%80%81%E8%AF%AD%E9%9F%B3)

        :返回:
          - `bool`: 能否发送语音
        """
        return (await self.call("can_send_record")).get("yes", False)

    async def get_version_info(self) -> VersionInfo:
        """
        :说明: `get_version_info`
        > [**获取版本信息**](https://docs.go-cqhttp.org/api/#%E8%8E%B7%E5%8F%96%E7%89%88%E6%9C%AC%E4%BF%A1%E6%81%AF), 返回值内删去了无用的固定值

        :返回:
          - `VersionInfo`: 版本信息，字段见GOCQ文档
        """
        return VersionInfo(**(await self.call("get_version_info")))

    async def check_url_safely(self, url: str) -> int:
        """
        :说明: `check_url_safely`
        > [**检查URL安全等级**](https://docs.go-cqhttp.org/api/#%E6%A3%80%E6%9F%A5%E9%93%BE%E6%8E%A5%E5%AE%89%E5%85%A8%E6%80%A7)

        :参数:
          * `url: str`: 需要检查的URL

        :返回:
          - `int`:安全等级, 1: 安全 2: 未知 3: 危险
        """
        return (await self.call("check_url_safely", url=url)).get("level", 2)

    async def get_group_file_system_info(
        self, group_id: Union[int, str]
    ) -> GroupFileSystemInfo:
        """
        :说明: `get_group_file_system_info`
        > [**获取群文件系统信息**](https://docs.go-cqhttp.org/api/#%E8%8E%B7%E5%8F%96%E7%BE%A4%E6%96%87%E4%BB%B6%E7%B3%BB%E7%BB%9F%E4%BF%A1%E6%81%AF)

        :参数:
          * `group_id: Union[int, str]`: 群号

        :返回:
          - `GroupFileSystemInfo`: 群文件系统信息，字段见GOCQ文档
        """
        r = await self.call("get_group_file_system_info", group_id=group_id)
        return GroupFileSystemInfo(**r)

    async def get_group_root_files(self, group_id: Union[int, str]) -> FileInfo:
        """
        :说明: `get_group_root_files`
        > [**获取群根目录文件列表**](https://docs.go-cqhttp.org/api/#%E8%8E%B7%E5%8F%96%E7%BE%A4%E6%A0%B9%E7%9B%AE%E5%BD%95%E6%96%87%E4%BB%B6%E5%88%97%E8%A1%A8)

        :参数:
          * `group_id: Union[int, str]`: 群号

        :返回:
          - `FileInfo`: 文件/文件夹列表，字段见GOCQ文档
        """
        return FileInfo(**(await self.call("get_group_root_files", group_id=group_id)))

    async def get_group_files_by_folder(
        self, group_id: Union[int, str], folder_id: int
    ) -> FileInfo:
        """
        :说明: `get_group_files_by_folder`
        > [**获取群子目录文件列表**](https://docs.go-cqhttp.org/api/#%E8%8E%B7%E5%8F%96%E7%BE%A4%E5%AD%90%E7%9B%AE%E5%BD%95%E6%96%87%E4%BB%B6%E5%88%97%E8%A1%A8)

        :参数:
          * `group_id: Union[int, str]`: 群号
          * `folder_id: int`: 文件夹ID 参考 Folder 对象

        :返回:
          - `FileInfo`: 文件/文件夹列表，字段见GOCQ文档
        """
        return FileInfo(
            **(
                await self.call(
                    "get_group_files_by_folder", group_id=group_id, folder_id=folder_id
                )
            )
        )

    async def get_group_file_url(
        self, group_id: Union[int, str], file_id: int, busid: int
    ) -> str:
        """
        :说明: `get_group_file_url`
        > [**获取群文件资源链接**](https://docs.go-cqhttp.org/api/#%E8%8E%B7%E5%8F%96%E7%BE%A4%E6%96%87%E4%BB%B6%E8%B5%84%E6%BA%90%E9%93%BE%E6%8E%A5)

        :参数:
          * `group_id: Union[int, str]`: 群号
          * `file_id: int`: 文件ID 参考 File 对象
          * `busid: int`: 文件类型 参考 File 对象

        :返回:
          - `str`: 文件下载链接
        """
        return (
            await self.call(
                "get_group_file_url", group_id=group_id, file_id=file_id, busid=busid
            )
        ).get("url", "")

    async def get_status(self) -> Status:
        """
        :说明: `get_status`
        > [**获取状态**](https://docs.go-cqhttp.org/api/#%E8%8E%B7%E5%8F%96%E7%8A%B6%E6%80%81)

        :返回:
          - `Status`: 状态，字段见GOCQ文档
        """
        return Status(**(await self.call("get_status")))

    async def get_group_at_all_remain(self, group_id: Union[int, str]) -> AtAllRemain:
        """
        :说明: `get_group_at_all_remain`
        > [**获取群 @全体成员 剩余次数**](https://docs.go-cqhttp.org/api/#%E8%8E%B7%E5%8F%96%E7%BE%A4-%E5%85%A8%E4%BD%93%E6%88%90%E5%91%98-%E5%89%A9%E4%BD%99%E6%AC%A1%E6%95%B0)

        :参数:
          * `group_id: Union[int, str]`: 群号

        :返回:
          - `AtAllRemain`: 剩余次数情况，字段见GOCQ文档
        """
        return AtAllRemain(
            **(await self.call("get_group_at_all_remain", group_id=group_id))
        )

    async def get_vip_info(self, user_id: Union[int, str]) -> VipInfo:
        """
        :说明: `get_vip_info`
        > [**获取VIP信息**](https://docs.go-cqhttp.org/api/#%E8%8E%B7%E5%8F%96vip%E4%BF%A1%E6%81%AF)

        :参数:
          * `user_id: Union[int, str]`: QQ号

        :返回:
          - `VipInfo`: VIP信息，字段见GOCQ文档
        """
        return VipInfo(**(await self.call("get_vip_info", user_id=user_id)))

    async def get_online_clients(self, no_cache: bool = False) -> List[Device]:
        """
        :说明: `get_online_clients`
        > [**获取当前账号在线客户端列表**](https://docs.go-cqhttp.org/api/#%E8%8E%B7%E5%8F%96%E5%BD%93%E5%89%8D%E8%B4%A6%E5%8F%B7%E5%9C%A8%E7%BA%BF%E5%AE%A2%E6%88%B7%E7%AB%AF%E5%88%97%E8%A1%A8)

        :可选参数:
          * `no_cache: bool = False`: 是否无视缓存

        :返回:
          - `List[Device]`: 在线客户端列表，字段见GOCQ文档
        """
        return [
            Device(**d)
            for d in (
                (await self.call("get_online_clients", no_cache=no_cache))["clients"]
            )
        ]

    async def get_essence_msg_list(self, group_id: Union[int, str]) -> List[EssenceMsg]:
        """
        :说明: `get_essence_msg_list`
        > [**获取精华消息列表**](https://docs.go-cqhttp.org/api/#%E8%8E%B7%E5%8F%96%E7%B2%BE%E5%8D%8E%E6%B6%88%E6%81%AF%E5%88%97%E8%A1%A8)

        :参数:
          * `group_id: Union[int, str]`: 群号

        :返回:
          - `List[EssenceMsg]`: 精华消息列表，字段见GOCQ文档
        """
        return [
            EssenceMsg(**e)
            for e in (await self.call("get_essence_msg_list", group_id=group_id))
        ]

    async def get_image(self, file: str) -> ImageInfo:
        """
        :说明: `get_image`
        > [**获取图片信息**](https://docs.go-cqhttp.org/api/#%E8%8E%B7%E5%8F%96%E5%9B%BE%E7%89%87%E4%BF%A1%E6%81%AF)

        :参数:
          * `file: str`: 图片缓存文件名，可在上报CQ码中获取

        :返回:
          - `ImageInfo`: 图片信息，字段见GOCQ文档
        """
        return ImageInfo(**(await self.call("get_image", file=file)))

    async def ocr_image(self, image: str) -> OCRResult:
        """
        :说明: `ocr_image`
        > [**图片 OCR**](https://docs.go-cqhttp.org/api/#%E5%9B%BE%E7%89%87-ocr)

        :参数:
          * `image: str`: 图片ID

        :返回:
          - `OCRResult`: OCR结果，字段见GOCQ文档
        """
        return OCRResult(**(await self.call("ocr_image", image=image)))

    async def download_file(
        self, url: str, thread_count: int, headers: Union[str, dict]
    ) -> str:
        """
        :说明: `download_file`
        > [**下载文件到缓存目录**](https://docs.go-cqhttp.org/api/#%E4%B8%8B%E8%BD%BD%E6%96%87%E4%BB%B6%E5%88%B0%E7%BC%93%E5%AD%98%E7%9B%AE%E5%BD%95)

        :参数:
          * `url: str`: 下载地址
          * `thread_count: int`: 下载线程数
          * `headers: Union[str, dict]`: 请求头，可以是字符串或字典

        :返回:
          - `str`: 下载到的绝对路径
        """
        return (
            await self.call(
                "download_file", url=url, thread_count=thread_count, headers=headers
            )
        )["file"]
