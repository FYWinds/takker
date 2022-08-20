# 从真寻那抄来的
import io
import textwrap

from PIL import Image, ImageDraw, ImageFont
from nonebot import on_command
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import Bot, MessageEvent

from utils.msg_util import image
from configs.path_config import FONT_PATH, IMAGE_PATH

__permission__ = 3
__plugin_name__ = "鲁迅说"
__plugin_usage__ = f"""
{'鲁迅说|鲁迅说过 <要说的话>':24s} | 返回一张鲁迅说过 xxxx 的图片
"""
__plugin_author__ = "风屿"
__plugin_version__ = "1.0.0"

luxun = on_command("鲁迅说过", aliases={"鲁迅说"}, priority=20)


@luxun.handle()
async def handle(bot: Bot, event: MessageEvent, state: T_State):
    args = event.get_plaintext()
    if args:
        state["content"] = args if args else "烦了，不说了"


@luxun.got("content", prompt="你让鲁迅说点啥?")
async def handle_event(bot: Bot, event: MessageEvent, state: T_State):
    content = state["content"].strip()
    if content.startswith(",") or content.startswith("，"):
        content = content[1:]
    if len(content) > 20:
        await luxun.finish("太长了, 鲁迅说不完!", at_sender=True)
    else:
        if len(content) >= 12:
            content = content[:12] + "\n" + content[12:]
        img = image(c=process_pic(content))
        await luxun.send(img)


def process_pic(content) -> bytes:
    text = content
    para = textwrap.wrap(text, width=15)
    MAX_W = 480
    bk_img = Image.open(IMAGE_PATH + "other/luxun.jpg")
    font_path = FONT_PATH + "/msyh.ttf"
    font = ImageFont.truetype(font_path, 37)
    font2 = ImageFont.truetype(font_path, 30)
    draw = ImageDraw.Draw(bk_img)
    current_h, pad = 300, 10
    for line in para:
        w, h = draw.textsize(line, font=font)
        draw.text(((MAX_W - w) / 2, current_h), line, font=font)
        current_h += h + pad
    draw.text((320, 400), "——鲁迅", font=font2, fill=(255, 255, 255))
    temp: io.BytesIO = io.BytesIO()
    bk_img.save(temp, format="PNG")
    result: bytes = temp.getvalue()
    return result
