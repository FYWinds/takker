import base64
from io import BytesIO

from nonebot.plugin import on_command
from nonebot.adapters.cqhttp import Bot, MessageEvent, MessageSegment

from configs.config import WEATHER_DEFAULT
from utils.msg_util import image

from .convert_pic import Image, draw
from .get_weather import get_City_Weather

__permission__ = 2
__plugin_name__ = "天气"
__usage__ = "天气 [城市]"

weather = on_command("天气", priority=1)


def img_to_b64(pic: Image.Image) -> str:
    buf = BytesIO()
    pic.save(buf, format="PNG")
    base64_str = base64.b64encode(buf.getbuffer()).decode()
    return "base64://" + base64_str


@weather.handle()
async def _(bot: Bot, event: MessageEvent):
    city = str(event.get_message())
    if city:
        try:
            data = await get_City_Weather(city)
            img = draw(data)
            await weather.finish(image(c=img_to_b64(img)))
        except KeyError:
            await weather.finish("这个地方不在天气数据库中哦 >_<")
    elif WEATHER_DEFAULT:
        data = await get_City_Weather(WEATHER_DEFAULT)
        img = draw(data)
        await weather.finish(image(c=img_to_b64(img)))
    else:
        await weather.finish("地点是...空气吗?? >_<")
