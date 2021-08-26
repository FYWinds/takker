from typing import Optional

from service.http_api import api_get


async def send_private_msg(
    uid: int,
    message: str,
    gid: Optional[int] = None,
    auto_escape: Optional[bool] = False,
) -> int:
    """
    :说明: `send_private_msg`
    > 发送私聊消息

    :参数:
      * `uid: int`: 私聊对象QQ号
      * `message: str`: 消息内容

    :可选参数:
      * `gid: Optional[int]`: 发送临时会话时的发起群号，机器人需要时群主/管理员
      * `auto_escape: Optional[bool] = False`: 消息内容是否作为纯文本发送(不解析CQ码)，默认否

    :返回:
      - `int`: 消息id
    """
    if gid:
        r = await api_get(
            "send_private_msg",
            user_id=uid,
            group_id=gid,
            message=message,
            auto_escape=auto_escape,
        )
    else:
        r = await api_get(
            "send_private_msg",
            user_id=uid,
            message=message,
            auto_escape=auto_escape,
        )
    return r["message_id"]


async def send_group_msg(
    gid: int, message: str, auto_escape: Optional[bool] = False
) -> int:
    """
    :说明: `send_group_msg`
    > 发送群消息

    :参数:
      * `gid: int`: 群号
      * `message: str`: 消息内容

    :可选参数:
      * `auto_escape: Optional[bool] = False`: 消息内容是否作为纯文本发送(不解析CQ码)，默认否

    :返回:
      - `int`: 消息id
    """
    r = await api_get(
        "send_group_msg", group_id=gid, message=message, auto_escape=auto_escape
    )
    return r["message_id"]
