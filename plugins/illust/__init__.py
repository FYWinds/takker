__permission__ = 6

__plugin_name__ = "随机pixiv美图"

__usage__ = """pix <关键词> <-l NSFW等级>
NSFW等级: 0-全年龄 1-R15 2-R18"""

from zhconv import convert
from nonebot.plugin import on_shell_command
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import Bot, MessageEvent, GroupMessageEvent
from nonebot.adapters.cqhttp.event import GroupMessageEvent

from utils.msg_util import text, image, reply
from service.db.utils.illust_config import get_illust_config

from .parser import pic_parser, set_parser

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
            c = await get_illust_config()
            tags = convert(r["tags"], "zh-tw")
            message = (
                f"{r['title']}({r['pid']})\n作者: {r['author']}({r['uid']})\ntags: {tags}"
            )
            message = ""
            message += f"{r['title']} " if c["send_title"] else ""
            message += f"{r['pid']}\n"
            message += f"作者: {r['author']}({r['uid']})\n" if c["send_author"] else ""
            message += f"tags: {tags}" if c["send_tags"] else ""
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
                            + (image(byte=r["img_bytes"]) if c["send_image"] else None)
                            + text(message)
                        )
                        if isinstance(event, GroupMessageEvent)
                        else (
                            (image(byte=r["img_bytes"]) if c["send_image"] else None)
                            + text(message)
                        )
                    ),
                )
            elif r["nsfw"] == 2 and c["send_image"]:
                message += "\nR-18的图片不直接发送，请从链接自行获取"
                await bot.send(
                    event,
                    message=(
                        (reply(event.message_id) + text(message))
                        if isinstance(event, GroupMessageEvent)
                        else (text(message))
                    ),
                )
            if c["send_link"]:
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


pixset = on_shell_command("pixset", parser=set_parser, priority=20)


@pixset.handle()
async def _s(bot: Bot, event: MessageEvent, state: T_State):
    args = state["args"]
    if hasattr(args, "handle"):
        result = await args.handle(args)
        if result:
            current_config = await get_illust_config()
            c: list[str] = []
            for n in current_config.keys():
                c.append(f"{n}, {'开启' if current_config[n] else '关闭'}")
            await pic.finish(result + "\n当前配置:\n" + "\n".join(c))
