from typing import Any, Optional

from .call_api import call


async def get_login_info() -> dict[Any, Any]:
    """
    :说明: `login_info`
    > 获取登录账号信息

    :返回:
      - `dict[Any, Any]`: 响应数据 参考GOCQ文档
    """
    r = await call("get_login_info")
    return r


async def get_stranger_info(uid: int, no_cache: Optional[bool] = True) -> dict[Any, Any]:
    """
    :说明: `stranger_info`
    > 获取陌生人信息

    :参数:
      * `uid: int`: QQ号

    :可选参数:
      * `no_cache: bool = True`: 是否不使用GOCQ端本地缓存的信息，默认不使用缓存

    :返回:
      - `dict[Any, Any]`: 响应数据 参考GOCQ文档
    """
    r = await call("get_stranger_info", user_id=uid, no_cache=no_cache)
    return r


async def get_group_info(gid: int, no_cache: Optional[bool] = True) -> dict[Any, Any]:
    """
    :说明: `group_info`
    > 获取群信息

    :参数:
      * `gid: int`: 群号

    :可选参数:
      * `no_cache: Optional[bool] = True`: 是否不使用GOCQ端本地缓存的信息，默认不使用缓存

    :返回:
      - `dict[Any, Any]`: 响应数据 参考GOCQ文档
    """
    r = await call("get_group_info", group_id=gid, no_cache=no_cache)
    return r


async def get_friend_list() -> dict[Any, Any]:
    """
    :说明: `friend_list`
    > 获取好友列表

    :返回:
      - `dict[Any, Any]`: 响应数据 参考GOCQ文档
    """
    r = await call("get_friend_list")
    return r


async def get_group_list() -> dict[Any, Any]:
    """
    :说明: `group_list`
    > 获取群列表

    :返回:
      - `dict[Any, Any]`: 响应数据 参考GOCQ文档
    """
    r = await call("get_group_list")
    return r


async def get_group_member_info(gid: int) -> dict[Any, Any]:
    """
    :说明: `group_member_info`
    > 获取群成员信息

    :参数:
      * `gid: int`: 群号

    :返回:
      - `dict[Any, Any]`: 响应数据 参考GOCQ文档
    """
    r = await call("get_group_member_list", group_id=gid)
    return r


async def get_group_member_list(gid: int) -> dict[Any, Any]:
    """
    :说明: `group_member_list`
    > 获取群成员列表，返回数据量较获取群成员信息少

    :参数:
      * `gid: int`: 群号

    :返回:
      - `dict[Any, Any]`: 响应数据 参考GOCQ文档
    """
    r = await call("get_group_member_list", group_id=gid)
    return r


async def group_honor_info(gid: int, type: Optional[str] = "all") -> dict[Any, Any]:
    """
    :说明: `group_honor_info`
    > 获取群荣誉信息

    :参数:
      * `gid: int`: 群号

    :可选参数:
      * `type: Optional[str] = "all"`: 群荣誉类型
      可选`talkative` `performer` `legend` `strong_newbie` `emotion`
      默认获取全部

    :返回:
      - `dict[Any, Any]`: 响应数据 参考GOCQ文档
    """


async def group_join_request() -> dict[Any, Any]:
    """
    :说明: `group_join_request`
    > 获取加群申请列表

    :返回:
      - `dict[Any, Any]`: 响应数据 参考GOCQ文档
    """
    r = await call("get_group_system_msg")
    return r["join_requests"]


async def group_invite_request() -> dict[Any, Any]:
    """
    :说明: `group_invite_request`
    > 获取被邀请进群列表

    :返回:
      - `dict[Any, Any]`: 响应数据 参考GOCQ文档
    """
    r = await call("get_group_system_msg")
    return r["invited_requests"]


async def version_info() -> dict[Any, Any]:
    """
    :说明: `version_info`
    > 获取GOCQ版本信息

    :返回:
      - `dict[Any, Any]`: 响应数据 参考GOCQ文档
    """
    r = await call("get_version_info")
    return r
