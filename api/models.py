from typing import List, Literal, Optional

import httpx
from pydantic import BaseModel
from nonebot.adapters.cqhttp import Message, MessageSegment, GroupMessageEvent
from nonebot.adapters.cqhttp.event import Sender


class SelfGroupMessage(GroupMessageEvent):
    post_type: Literal["message_sent"]


class MessageGot(BaseModel):
    message_id: int
    real_id: int
    sender: Sender
    time: int
    message: Message
    raw_message: str


class GroupMessageGot(MessageGot):
    group_id: int
    message_type: Literal["group"]


class BaseUserInfo(BaseModel):
    user_id: int
    nickname: str


class UserInfo(BaseUserInfo):
    login_days: int
    level: int
    sex: Literal["male", "female", "unknown"]
    age: int
    qid: str
    avatar: Optional[str] = None

    async def get_user_avatar(self) -> bytes:
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"https://p.qlogo.cn/gh/{self.user_id}/100")
        return resp.content


class FriendInfo(BaseUserInfo):
    remark: str


class GroupInfo(BaseModel):
    group_id: int
    group_name: str
    group_memo: str
    group_create_time: int
    group_level: int
    member_count: int
    max_member_count: int

    async def get_group_avatar(self) -> bytes:
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                f"https://p.qlogo.cn/gh/{self.group_id}/{self.group_id}/100"
            )
        return resp.content


class GroupMemberInfo(BaseUserInfo):
    group_id: int
    card: str
    sex: Literal["male", "female", "unknown"]
    age: int
    card_changeable: bool
    area: str
    join_time: int
    last_sent_time: int
    level: int
    role: Literal["owner", "admin", "member"]
    unfriendly: bool
    title: str
    title_expire_time: int
    shut_up_timestamp: int


class Honor(BaseUserInfo):
    discription: str
    day_count: Optional[int] = None


class HonorInfo(BaseModel):
    group_id: int
    current_talkative: Optional[List[Honor]] = None
    talkative_list: Optional[List[Honor]] = None
    performer_list: Optional[List[Honor]] = None
    legend_list: Optional[List[Honor]] = None
    strong_newbie_list: Optional[List[Honor]] = None
    emotion_list: Optional[List[Honor]] = None


class Request(BaseModel):
    request_id: int
    group_id: int
    group_name: str
    checked: bool
    actor: int


class InvitedRequest(Request, BaseModel):
    invitor_uin: int
    invitor_nick: str


class JoinRequest(Request, BaseModel):
    requester_uin: int
    requester_nick: str
    remark: str
    message: str
    suspicious: bool


class GroupSystemMsg(BaseModel):
    invited_requests: Optional[List[InvitedRequest]] = None
    join_requests: Optional[List[JoinRequest]] = None


class GroupFileSystemInfo(BaseModel):
    group_id: int
    file_count: int
    limit_count: int
    used_spacee: int
    total_space: int


class File(BaseModel):
    group_id: int
    file_id: int
    file_name: str
    busid: int
    file_size: int
    upload_time: int
    dead_time: int
    modify_time: int
    download_times: int
    uploader: int
    uploader_name: str


class Folder(BaseModel):
    group_id: int
    folder_id: int
    folder_name: str
    create_time: int
    creator: int
    creator_name: str
    total_file_count: int


class FileInfo(BaseModel):
    files: Optional[List[File]] = None
    folders: Optional[List[Folder]] = None


class Statictics(BaseModel):
    packet_received: int
    packet_sent: int
    packet_lost: int
    message_received: int
    message_sent: int
    disconnect_times: int
    lost_times: int


class Status(BaseModel):
    app_initialized: bool
    app_enabled: bool
    plugins_good: bool
    app_good: bool
    online: bool
    good: bool
    stat: Statictics


class AtAllRemain(BaseModel):
    can_at_all: bool
    remain_at_all_count_for_group: int
    remain_at_all_count_for_uin: int


class VipInfo(BaseUserInfo):
    level: int
    level_speed: float
    vip_level: str
    vip_growth_speed: int
    vip_growth_total: int


class Device(BaseModel):
    app_id: int
    device_name: str
    device_kind: str


class EssenceMsg(BaseModel):
    sender_id: int
    sender_nick: str
    sender_time: int
    operator_id: int
    operator_nick: str
    operator_time: int
    message_id: int


class ForwardMsg(BaseModel):
    content: List[MessageSegment]
    sender: Sender
    time: int


class ImageInfo(BaseModel):
    file: str
    filename: str
    size: int
    url: str


class VersionInfo(BaseModel):
    app_name: Literal["go-cqhttp"]
    app_version: str
    app_full_name: str
    runtime_version: str
    runtime_os: str
    version: str
    protocol: int


class OCRCoordinates(BaseModel):
    x: int
    y: int


class OCRText(BaseModel):
    text: str
    confidence: int
    coordinates: List[OCRCoordinates]


class OCRResult(BaseModel):
    language: str
    texts: List[OCRText]


__all__ = [
    "SelfGroupMessage",
    "MessageGot",
    "GroupMessageGot",
    "BaseUserInfo",
    "UserInfo",
    "FriendInfo",
    "GroupInfo",
    "GroupMemberInfo",
    "HonorInfo",
    "GroupSystemMsg",
    "GroupFileSystemInfo",
    "FileInfo",
    "Status",
    "AtAllRemain",
    "VipInfo",
    "Device",
    "EssenceMsg",
    "ForwardMsg",
    "ImageInfo",
    "VersionInfo",
    "OCRResult",
]
