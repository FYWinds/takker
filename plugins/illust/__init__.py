from zhconv import convert
from nonebot.plugin import on_shell_command
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import Bot, MessageEvent, GroupMessageEvent

from utils.msg_util import text, image, reply
from db.utils.illust_config import IllustConfig

from .parser import pic_parser, set_parser

__plugin_info__ = {
    "name": "Pixiv美图",
    "des": "从Bot的数据库中随机抽取一张来自于Pixiv的美图",
    "usage": {
        "pix": {"des": "返回一张全年龄图片"},
        "pix -l <等级>": {"des": "返回一张指定等级的图片", "eg": "pix -l 1"},
        "pix <关键词>": {"des": "返回一张指定关键词的图片", "eg": "pix 初音未来 miku -l 2"},
    },
    "additional_info": """
等级 0->全年龄,1->R-15,2->R18
等级默认为0，可与关键词同时使用
关键词可输入多个，用空格隔开，为与的关系
""".strip(),
    "author": "风屿",
    "version": "1.0.0",
    "permission": 6,
}

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
            c = await IllustConfig.get_illust_config()
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
                            + (image(c=r["img_bytes"]) if c["send_image"] else None)
                            + text(message)
                        )
                        if isinstance(event, GroupMessageEvent)
                        else (
                            (image(c=r["img_bytes"]) if c["send_image"] else None)
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
            current_config = await IllustConfig.get_illust_config()
            c: list[str] = []
            for n in current_config.keys():
                c.append(f"{n}, {'开启' if current_config[n] else '关闭'}")
            await pic.finish(result + "\n当前配置:\n" + "\n".join(c))
