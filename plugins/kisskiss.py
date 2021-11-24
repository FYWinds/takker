from io import BytesIO

import httpx
import numpy
from PIL import Image as IMG
from PIL import ImageOps, ImageDraw
from nonebot import on_command
from moviepy.editor import ImageSequenceClip as imageclip
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import GROUP, Bot, MessageEvent

from utils.browser import get_ua
from utils.msg_util import MS
from configs.path_config import IMAGE_PATH

__plugin_info__ = {
    "name": "亲亲",
    "des": "动图生成",
    "usage": {
        "亲 @目标": "返回一张你和目标的亲亲动图",
    },
    "author": "风屿",
    "version": "1.0.0",
    "permission": 2,
}
kiss = on_command("亲", permission=GROUP, priority=20)


@kiss.handle()
async def handle_receive(bot: Bot, event: MessageEvent, state: T_State):
    at = str(event.message).strip("[CQ:at,qq=] ")
    if not at.isdigit():
        return
    member_id = str(event.user_id)
    SavePic = f"tempKiss-{member_id}-{at}.gif"
    await tie(member_id, at)
    await kiss.finish(MS.image(SavePic, "kisskiss"))


async def save_gif(gif_frames, dest, fps=25):
    clip = imageclip(gif_frames, fps=fps)
    clip.write_gif(dest)
    clip.close()


async def kiss_make_frame(operator, target, i):
    operator_x = [92, 135, 84, 80, 155, 60, 50, 98, 35, 38, 70, 84, 75]
    operator_y = [64, 40, 105, 110, 82, 96, 80, 55, 65, 100, 80, 65, 65]
    target_x = [58, 62, 42, 50, 56, 18, 28, 54, 46, 60, 35, 20, 40]
    target_y = [90, 95, 100, 100, 100, 120, 110, 100, 100, 100, 115, 120, 96]
    bg = IMG.open(f"{IMAGE_PATH}kisskiss/KissFrames/{i}.png")
    gif_frame = IMG.new("RGB", (200, 200), (255, 255, 255))
    gif_frame.paste(bg, (0, 0))
    gif_frame.paste(target, (target_x[i - 1], target_y[i - 1]), target)
    gif_frame.paste(operator, (operator_x[i - 1], operator_y[i - 1]), operator)
    return numpy.array(gif_frame)


async def tie(operator_id, target_id) -> None:
    operator_url = f"http://q1.qlogo.cn/g?b=qq&nk={str(operator_id)}&s=640"
    target_url = f"http://q1.qlogo.cn/g?b=qq&nk={str(target_id)}&s=640"
    gif_frames = []
    async with httpx.AsyncClient(headers=get_ua()) as client:
        resp = await client.get(url=operator_url)
    operator_img = resp.read()
    operator = IMG.open(BytesIO(operator_img))

    async with httpx.AsyncClient(headers=get_ua()) as client:
        resp = await client.get(url=target_url)
    target_img = resp.read()
    target = IMG.open(BytesIO(target_img))

    operator = operator.resize((40, 40), IMG.ANTIALIAS)
    size = operator.size
    r2 = min(size[0], size[1])
    circle = IMG.new("L", (r2, r2), 0)
    draw = ImageDraw.Draw(circle)
    draw.ellipse((0, 0, r2, r2), fill=255)
    alpha = IMG.new("L", (r2, r2), 255)
    alpha.paste(circle, (0, 0))
    operator.putalpha(alpha)

    target = target.resize((50, 50), IMG.ANTIALIAS)
    size = target.size
    r2 = min(size[0], size[1])
    circle = IMG.new("L", (r2, r2), 0)
    draw = ImageDraw.Draw(circle)
    draw.ellipse((0, 0, r2, r2), fill=255)
    alpha = IMG.new("L", (r2, r2), 255)
    alpha.paste(circle, (0, 0))
    target.putalpha(alpha)

    for i in range(1, 14):
        gif_frames.append(await kiss_make_frame(operator, target, i))
    await save_gif(
        gif_frames,
        f"{IMAGE_PATH}kisskiss/tempKiss-{operator_id}-{target_id}.gif",
        fps=25,
    )
