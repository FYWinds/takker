
from configs.config import OWNER, SUPERUSERS
from nonebot.plugin import on_message, on_request
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import (PRIVATE_FRIEND, Bot, GroupRequestEvent,
                                     FriendRequestEvent, PrivateMessageEvent)

__permission__ = 0

friend_request = on_request(priority=1)
requests: dict[str, str] = {}


@friend_request.handle()
async def _frh(bot: Bot, event: FriendRequestEvent, state: T_State):
    global requests
    if not isinstance(event, FriendRequestEvent):
        await friend_request.finish()
    if str(event.user_id) in SUPERUSERS or str(event.user_id) in OWNER:
        await bot.set_friend_add_request(flag=event.flag, approve=True)
    else:
        user = OWNER
        message = f"收到来自({event.user_id})的好友请求，验证消息为：{event.comment}"
        result = await bot.send_private_msg(user_id=int(user), message=message)
        requests |= {str(result["message_id"]): event.flag}


group_request = on_request(priority=1)


@group_request.handle()
async def _grh(bot: Bot, event: GroupRequestEvent, state: T_State):
    if event.sub_type == "invite":
        if str(event.user_id) in SUPERUSERS or str(event.user_id) in OWNER:
            await bot.set_group_add_request(
                flag=event.flag, sub_type="invite", approve=True
            )


checker = on_message(priority=100, permission=PRIVATE_FRIEND, block=False)


@checker.handle()
async def _ch(bot: Bot, event: PrivateMessageEvent, state: T_State):
    global requests
    if str(event.user_id) not in OWNER:
        await checker.finish()
    if not event.reply:
        await checker.finish()
    assert event.reply is not None
    reply_id = str(event.reply.message_id)
    if reply_id not in requests.keys():
        return
    text = event.message.extract_plain_text()
    if text in ["可", "通过"]:
        await bot.set_friend_add_request(flag=requests[reply_id], approve=True)
        requests.pop(reply_id)
        await checker.finish("成功通过请求")
    elif text in ["不可", "爬", "不通过"]:
        await bot.set_friend_add_request(flag=requests[reply_id], approve=False)
        requests.pop(reply_id)
        await checker.finish("成功拒绝请求")
    else:
        await checker.finish("处理失败，请使用 可/不可 来选择是否通过请求")
