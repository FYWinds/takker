from io import BytesIO

import httpx
from nonebot import on_command
from nonebot.adapters.cqhttp import Bot, MessageEvent
from nonebot.adapters.cqhttp.event import GroupMessageEvent

from utils.img_util import ImageUtil
from utils.msg_util import image

__permission__ = 3
__plugin_name__ = "我有个朋友"
__plugin_usage__ = f"""
{'我有个朋友 @某人 <他想说的话>':24s} | 伪造一张朋友发来消息的图片
{'我有个朋友 @某人 说<他想说的话>':24s} | 伪造一张朋友发来消息的图片
我有个朋友可替换为以下命令:
    我有一个朋友
    我有朋友
    我有个朋友说
"""
__plugin_author__ = "风屿"
__plugin_version__ = "1.0.0"

friend = on_command("我有个朋友", aliases={"我有一个朋友", "我有朋友", "我有个朋友说"}, priority=20)


@friend.handle()
async def _(bot: Bot, event: MessageEvent):
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
        at_user = await bot.get_group_member_info(group_id=event.group_id, user_id=at)
        user_name = at_user["card"] if at_user["card"] else at_user["nickname"]
    else:
        user_name = (await bot.get_stranger_info(user_id=at))["nickname"]

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

    await friend.finish(image(c=img.toB64()))
