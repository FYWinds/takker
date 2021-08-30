__permission__ = 6

__plugin_name__ = "随机pixiv美图"

__usage__ = """pix <关键词> <-l NSFW等级>
NSFW等级: 0-全年龄 1-R15 2-R18"""

from nonebot.adapters.cqhttp.event import GroupMessageEvent
from zhconv import convert

from nonebot.adapters.cqhttp import (
    Bot,
    MessageEvent,
    GroupMessageEvent,
    PrivateMessageEvent,
)
from nonebot.plugin import on_shell_command
from nonebot.typing import T_State

from utils.utils import Processing
from utils.msg_util import image, text, reply

from .parser import pic_parser

pic = on_shell_command("pix", parser=pic_parser, priority=20)


@pic.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    args = state["args"]
    args.user = event.user_id
    args.group = event.group_id if isinstance(event, GroupMessageEvent) else None

    if hasattr(args, "handle"):
        result = await args.handle(args)
        if result:
            r = result
            tags = convert(r["tags"], "zh-tw")
            message = (
                f"{r['title']}({r['pid']})\n作者: {r['author']}({r['uid']})\ntags: {tags}"
            )
            if r["is_search"]:
                await bot.send(
                    event,
                    message=(
                        (reply(event.message_id) + text(message))
                        if isinstance(event, GroupMessageEvent)
                        else (text(message))
                    ),
                )
            if r["nsfw"] in [0, 1]:
                await bot.send(
                    event,
                    message=(
                        (
                            reply(event.message_id)
                            + image(byte=r["img_bytes"])
                            + text(message)
                        )
                        if isinstance(event, GroupMessageEvent)
                        else (image(byte=r["img_bytes"]) + text(message))
                    ),
                )
            elif r["nsfw"] == 2:
                message += "\nR-18的图片不直接发送，请从链接自行获取"
                await bot.send(
                    event,
                    message=(
                        (reply(event.message_id) + text(message))
                        if isinstance(event, GroupMessageEvent)
                        else (text(message))
                    ),
                )
            orig = "图片链接（请复制后使用浏览器查看）:"
            for i in r["orig_img_url"]:
                orig += f"\n{i}"
            await bot.send(
                event,
                message=(
                    (reply(event.message_id) + text(orig))
                    if isinstance(event, GroupMessageEvent)
                    else text(orig)
                ),
            )
        else:
            await pic.finish(reply(event.message_id) + text("未找到符合要求的图片"))
