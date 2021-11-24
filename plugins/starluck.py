import os
import time
import textwrap

import httpx
import pypinyin
from PIL import Image, ImageDraw, ImageFont
from nonebot import on_command
from nonebot.log import logger
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import Bot, MessageEvent, GroupMessageEvent

from configs.config import ALI_API_TOKEN
from utils.msg_util import MS
from db.utils.starluck import Starluck
from configs.path_config import FONT_PATH, IMAGE_PATH

__plugin_info__ = {
    "name": "星座运势",
    "des": "每个星座每日的详细运势",
    "usage": {
        ".sluck|sluck|星座运势": "返回你绑定的星座的当日运势",
        ".sluck|sluck|星座运势 <星座>": {"des": "绑定一个星座，返回这个星座的当日运势", "eg": ".sluck 双鱼座"},
    },
    "author": "风屿",
    "version": "1.0.0",
    "permission": 1,
}


starluck = on_command(
    ".sluck",
    priority=20,
    aliases={
        "星座运势",
        "sluck",
    },
)


@starluck.handle()
async def handle_starluck_receive(bot: Bot, event: MessageEvent, state: T_State):
    star = str(event.get_message()).strip()
    user_id = event.user_id
    stars = [
        "baiyang",
        "jinniu",
        "shuangzi",
        "juxie",
        "shizi",
        "chunv",
        "tiancheng",
        "tianxie",
        "sheshou",
        "mojie",
        "shuiping",
        "shuangyu",
    ]
    stars_cn = ["白羊", "金牛", "双子", "巨蟹", "狮子", "处女", "天秤", "天蝎", "射手", "摩羯", "水瓶", "双鱼"]

    if not len(star) == 0:
        # 判断是否有星座名称存在
        star = star.replace("座", "")
        star_pinyin = ""
        for i in pypinyin.pinyin(star, style=pypinyin.NORMAL):
            star_pinyin += "".join(i)

        # 判断是否合法
        if star_pinyin not in stars:
            message = (
                (MS.reply(user_id) + MS.text("请输入正确的星座名称"))
                if isinstance(event, GroupMessageEvent)
                else MS.text("请输入正确的星座名称")
            )
            await starluck.finish(message)

        num = stars.index(star_pinyin) + 1
        await Starluck.set_star(user_id, num)
        message = (
            (MS.reply(user_id) + MS.text("绑定成功"))
            if isinstance(event, GroupMessageEvent)
            else MS.text("绑定成功")
        )
        await starluck.send(message)

    if not await Starluck.query_star(user_id):
        message = (
            (MS.reply(user_id) + MS.text("请使用\n.sluck 星座\n绑定星座"))
            if isinstance(event, GroupMessageEvent)
            else MS.text("请使用\n.sluck 星座\n绑定星座")
        )
        await starluck.finish(message)

    star_pinyin = stars[await Starluck.query_star(user_id) - 1]
    star = stars_cn[await Starluck.query_star(user_id) - 1]

    # 从缓存读取图片

    time_today = time.strftime("%Y-%m-%d")
    if await pre_process(star_pinyin):
        file = f"temp-{time_today}-{star_pinyin}.png"
        message = message = (
            (MS.reply(user_id) + MS.image(file, "starluck"))
            if isinstance(event, GroupMessageEvent)
            else MS.image(file, "starluck")
        )
        logger.debug("Cache Hit!")
        await starluck.finish(message)

    # 未缓存，生成当日12个星座的缓存
    await make_cache(stars, stars_cn)

    file = f"temp-{time_today}-{star_pinyin}.png"
    message = message = (
        (MS.reply(user_id) + MS.image(file, "starluck"))
        if isinstance(event, GroupMessageEvent)
        else MS.image(file, "starluck")
    )

    await starluck.finish(message)


async def pre_process(star_pinyin: str):
    time_today = time.strftime("%Y-%m-%d")
    file = f"{IMAGE_PATH}starluck/temp-{time_today}-{star_pinyin}.png"

    if os.path.exists(file):
        return True

    return False


async def get_data(star_pinyin: str):
    url = "https://ali-star-lucky.showapi.com/star"
    params = {
        "needMonth": 0,
        "needTomorrow": 0,
        "needWeek": 0,
        "needYear": 0,
        "star": star_pinyin,
    }
    headers = {"Authorization": f"APPCODE {ALI_API_TOKEN}"}

    async with httpx.AsyncClient() as client:
        response = await client.get(url=url, headers=headers, params=params)

    return response.json()


async def generate_content(resp_body: dict, star: str):
    money_star = str(resp_body["money_star"])
    money_txt = "财富运势：" + str(resp_body["money_txt"])

    love_star = str(resp_body["love_star"])
    love_txt = "爱情运势：" + str(resp_body["love_txt"])
    grxz = str(resp_body["grxz"])

    work_star = str(resp_body["work_star"])
    work_txt = "工作运势：" + str(resp_body["work_txt"])

    summary_star = str(resp_body["summary_star"])
    general_txt = "运势简评：" + str(resp_body["general_txt"])

    lucky_num = str(resp_body["lucky_num"])
    lucky_time = str(resp_body["lucky_time"])
    lucky_color = str(resp_body["lucky_color"])
    lucky_direction = str(resp_body["lucky_direction"])

    day_notice = str(resp_body["day_notice"])

    time_today = time.strftime("%Y-%m-%d")

    starluck_answer = ""
    starluck_answer += "星座运势\n" + "星座：" + star + "座"
    starluck_answer += "\n日期：" + time_today

    starluck_answer += "\n"

    starluck_answer += "\n爱情指数：" + love_star + "\n"
    starluck_answer += textwrap.fill(love_txt, width=30)
    starluck_answer += "\n相配星座：" + grxz

    starluck_answer += "\n"

    starluck_answer += "\n工作指数：" + work_star + "\n"
    starluck_answer += textwrap.fill(work_txt, width=30)

    starluck_answer += "\n"

    starluck_answer += "\n财富指数：" + money_star + "\n"
    starluck_answer += textwrap.fill(money_txt, width=30)

    starluck_answer += "\n"

    starluck_answer += "\n综合指数：" + summary_star + "\n"
    starluck_answer += textwrap.fill(general_txt, width=30)

    starluck_answer += "\n"

    starluck_answer += "\n幸运数字：" + lucky_num
    starluck_answer += "\n幸运颜色：" + lucky_color
    starluck_answer += "\n幸运方位：" + lucky_direction
    starluck_answer += "\n幸运时间：" + lucky_time

    starluck_answer += "\n今日注意：" + day_notice
    starluck_answer += "\n"

    return starluck_answer


async def generate_img(star_pinyin: str, content: str):
    im = Image.new("RGB", (450, 600), (255, 255, 255))
    draw = ImageDraw.Draw(im)
    font = ImageFont.truetype(os.path.join(FONT_PATH, "msyh.ttf"), 14)
    draw.text((10, 10), content, font=font, fill=(65, 83, 130))
    time_today = time.strftime("%Y-%m-%d")
    file = f"{IMAGE_PATH}starluck/temp-{time_today}-{star_pinyin}.png"
    im.save(file)


async def make_cache(stars, stars_cn):
    for i in range(0, 12):
        resp_body = (await get_data(stars[i]))["showapi_res_body"]["day"]
        content = await generate_content(resp_body, stars_cn[i])
        await generate_img(stars[i], content)
