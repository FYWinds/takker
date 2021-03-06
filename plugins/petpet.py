from io import BytesIO

import httpx
import numpy
from PIL import Image as IMG
from PIL import ImageOps
from nonebot import on_command
from moviepy.editor import ImageSequenceClip as imageclip
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import GROUP, Bot, MessageEvent

from utils.browser import get_ua
from utils.msg_util import image
from configs.path_config import IMAGE_PATH

__plugin_info__ = {
    "name": "Rua!",
    "des": "动图生成",
    "usage": {
        "摸|rua @目标": "返回一张摸目标头的动图",
    },
    "author": "风屿",
    "version": "1.0.0",
    "permission": 2,
}


pet = on_command(
    "摸",
    aliases={
        "rua",
        "摸摸",
    },
    priority=20,
    permission=GROUP,
)


@pet.handle()
async def handle_receive(bot: Bot, event: MessageEvent, state: T_State):
    at = str(event.message).strip("[CQ:at,qq=] ")
    if not at.isdigit():
        return
    await petpet(at)
    image_name = f"temp-{at}.gif"
    await pet.finish(image(image_name, "petpet"))


frame_spec = [
    (27, 31, 86, 90),
    (22, 36, 91, 90),
    (18, 41, 95, 90),
    (22, 41, 91, 91),
    (27, 28, 86, 91),
]

squish_factor = [
    (0, 0, 0, 0),
    (-7, 22, 8, 0),
    (-8, 30, 9, 6),
    (-3, 21, 5, 9),
    (0, 0, 0, 0),
]

squish_translation_factor = [0, 20, 34, 21, 0]

frames = tuple([f"{IMAGE_PATH}petpet/PetPetFrames/frame{i}.png" for i in range(5)])


async def save_gif(gif_frames, dest, fps=10):
    clip = imageclip(gif_frames, fps=fps)
    clip.write_gif(dest)
    clip.close()


async def make_frame(avatar, i, squish=0, flip=False):
    spec = list(frame_spec[i])
    for j, s in enumerate(spec):
        spec[j] = int(s + squish_factor[i][j] * squish)
    hand = IMG.open(frames[i])
    if flip:
        avatar = ImageOps.mirror(avatar)
    avatar = avatar.resize(
        (int((spec[2] - spec[0]) * 1.2), int((spec[3] - spec[1]) * 1.2)), IMG.ANTIALIAS
    )
    gif_frame = IMG.new("RGB", (112, 112), (255, 255, 255))
    gif_frame.paste(avatar, (spec[0], spec[1]))
    gif_frame.paste(hand, (0, int(squish * squish_translation_factor[i])), hand)
    return numpy.array(gif_frame)


async def petpet(member_id, flip=False, squish=0, fps=20) -> None:
    url = f"http://q1.qlogo.cn/g?b=qq&nk={str(member_id)}&s=640"
    gif_frames = []
    async with httpx.AsyncClient(headers=get_ua()) as client:
        resp = await client.get(url)
    img_content = resp.content

    avatar = IMG.open(BytesIO(img_content))

    for i in range(5):
        gif_frames.append(await make_frame(avatar, i, squish=squish, flip=flip))
    await save_gif(gif_frames, f"{IMAGE_PATH}petpet/temp-{member_id}.gif", fps=fps)
