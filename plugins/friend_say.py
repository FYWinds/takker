from io import BytesIO

import httpx
from gocqapi import api
from nonebot import on_command
from nonebot.adapters.cqhttp import Bot, MessageEvent
from nonebot.adapters.cqhttp.event import GroupMessageEvent

from utils.img_util import ImageUtil
from utils.msg_util import MS

__plugin_info__ = {
    "name": "我有个朋友",
    "des": "伪造一张朋友发来信息的图片",
    "usage": {
        "我有个朋友 @某人 <他要说的话>": {"des": "伪造一张朋友发来信息的图片", "eg": "我有个朋友 @群主 来点乐子"},
        "我有个朋友 @某人 说<他要说的话>": {"des": "伪造一张朋友发来信息的图片", "eg": "我有个朋友 @群主 说来点乐子"},
    },
    "addition_info": "我有个朋友可以替换为: 我有一个朋友|我有朋友|我有个朋友说",
    "author": "风屿",
    "version": "1.4.0",
    "permission": 3,
}


friend = on_command("我有个朋友", aliases={"我有一个朋友", "我有朋友", "我有个朋友说"}, priority=20)


@friend.handle()
async def _(bot: Bot, event: MessageEvent):
    at: int = int()
    text: str = str()
    for num, seg in enumerate(event.message):
        if seg.type == "at":
            at = seg.data["qq"]
            text = (
                event.message[num + 1].data["text"].strip()
                if num + 1 <= len(event.message)
                else ""
            )
            break

    if not at or not text:
        return

    text = text[1:] if text.startswith("说") else text

    # Get QQ Gravatar
    url = "https://q1.qlogo.cn/g?b=qq&nk={}&s=100".format(at)
    async with httpx.AsyncClient() as client:
        r = await client.get(url)
        avatar = r.content

    # Get QQ Name
    if isinstance(event, GroupMessageEvent):
        at_user = await api.get_group_member_info(group_id=event.group_id, user_id=at)
        user_name = at_user.card if at_user.card else at_user.nickname
    else:
        user_name = (await api.get_stranger_info(user_id=at)).nickname

    # Create image
    if avatar:
        ava = ImageUtil(100, 100, background=BytesIO(avatar))
    else:
        ava = ImageUtil(100, 100, color=(0, 0, 0))
    ava.circle()
    name = ImageUtil(300, 30, font_size=30)
    name.text((0, 0), user_name)
    img = ImageUtil(700, 150, font_size=25, color="white")
    img.paste(ava, (30, 25), alpha=True)
    img.paste(name, (150, 38))
    img.text((150, 85), text, (125, 125, 125))

    await friend.finish(MS.image(c=img.toB64()))
