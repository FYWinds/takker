from typing import Optional

from .call_api import call


async def kick(gid: int, uid: int, reject: Optional[bool] = False):
    """
    :说明: `kick`
    > 群组踢人

    :参数:
      * `gid: int`: 群号
      * `uid: int`: 踢出对象的QQ号

    :可选参数:
      * `reject: Optional[bool] = False`:是否拒绝再次加群，默认不拒绝
    """
    await call("set_group_kick", group_id=gid, user_id=uid, reject_add_request=reject)


async def ban_personal(gid: int, uid: int, duration: int):
    """
    :说明: `ban_personal`
    > 群组单人禁言

    :参数:
      * `gid: int`: 群号
      * `uid: int`: 禁言对象的QQ号
      * `duration: int`: 禁言时长，单位分钟
    """
    duration *= 60
    await call("set_group_ban", group_id=gid, user_id=uid, duration=duration)


async def ban_anonymous(gid: int, flag: str, duration: int):
    """
    :说明: `ban_anonymous`
    > 群组匿名用户禁言

    :参数:
      * `gid: int`: 群号
      * `flag: str`: 禁言对象的特征码，通常包含在MessageEvent中
      * `duration: int`: 禁言时长，单位分钟
    """
    duration *= 60
    await call(
        "set_group_anonymous_ban", group_id=gid, anonymous_flag=flag, duration=duration
    )


async def ban_all(gid: int, enable: Optional[bool] = True):
    """
    :说明: `ban_all`
    > 群组全体禁言

    :参数:
      * `gid: int`: 群号

    :可选参数:
      * `enable: Optional[bool] = True`: 是否开启禁言，默认开启
    """
    await call("set_group_whole_ban", group_id=gid, enable=enable)


async def set_group_admin(gid: int, uid: int, enable: Optional[bool] = True):
    """
    :说明: `set_group_admin`
    > 群组设置管理员

    :参数:
      * `gid: int`: 群号
      * `uid: int`: 设置为管理员对象的QQ号

    :可选参数:
      * `enable: Optional[bool] = True`: 是否设置，默认设置
    """
    await call("set_group_admin", group_id=gid, user_id=uid, enable=enable)


async def set_group_anonymous(gid: int, enable: Optional[bool] = True):
    """
    :说明: `set_group_anonymous`
    > 设置是否允许群组匿名聊天

    :参数:
      * `gid: int`: 群号

    :可选参数:
      * `enable: Optional[bool] = True`: 是否开启，默认允许
    """
    await call("set_group_anonymous", group_id=gid, enable=enable)


async def set_group_name(gid: int, name: str):
    """
    :说明: `set_group_name`
    > 设置群名

    :参数:
      * `gid: int`: 群号
      * `name: str`: 群名称
    """
    await call("set_group_name", group_id=gid, group_name=name)


async def set_title(gid: int, uid: int, title: Optional[str] = ""):
    """
    :说明: `set_title`
    > 设置群头衔

    :参数:
      * `gid: int`: 群号
      * `uid: int`: 设置对象的QQ号

    :可选参数:
      * `title: Optional[str] = ""`: 头衔内容，最多六个字，默认取消头衔
    """
    await call(
        "set_group_special_title",
        group_id=gid,
        user_id=uid,
        special_title=title,
        duration=-1,
    )


async def set_request(
    flag: str, approve: Optional[bool] = True, reason: Optional[str] = ""
):
    """
    :说明: `set_request`
    > 处理加群请求

    :参数:
      * `flag: str`: 请求特征码，参考`api.get_info.group_invite_request()`返回值

    :可选参数:
      * `approve: Optional[bool] = True`: 是否通过加群请求，默认通过
      * `reason: Optional[str] = ""`: 拒绝加群请求的原因
    """
    sub_type: str = "add"
    await call(
        "set_group_add_request",
        flag=flag,
        sub_type=sub_type,
        approve="true" if approve else "false",
        reason=reason,
    )


async def leave(gid: int, dismiss: Optional[bool] = False):
    """
    :说明: `leave`
    > 退出群组

    :参数:
      * `gid: int`: 群号

    :可选参数:
      * `dismiss: Optional[bool] = False`: 是否解散群聊，需要Bot具有群主身份，默认不解散
    """
    await call("set_group_leave", group_id=gid, is_dismiss=dismiss)
