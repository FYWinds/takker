# Author HibiKier/zhenxun_bot
# Edit by FYWinds
import os
from io import BytesIO
from typing import Union, Optional

import ujson
from nonebot.log import logger
from nonebot.adapters.cqhttp.message import MessageSegment

from configs.path_config import IMAGE_PATH, VOICE_PATH


class MS:
    @staticmethod
    def image(
        img_file: str = None,
        path: str = "",
        abspath: Optional[str] = None,
        c: Optional[Union[str, bytes, BytesIO]] = None,
    ) -> MessageSegment:
        if abspath:
            if os.path.exists(abspath):
                return MessageSegment.image("file:///" + abspath)
            else:
                return MS.text("")
        elif c:
            if isinstance(c, str):
                if c.find("base64://") != -1:
                    return MessageSegment.image(c)
                else:
                    return MessageSegment.image("base64://" + c)
            else:
                return MessageSegment.image(c)
        else:
            img_file = str(img_file)
            if img_file.find("http") == -1:
                if len(img_file.split(".")) == 1:
                    img_file += ".jpg"
                if os.path.exists(IMAGE_PATH + path + "/" + img_file):
                    return MessageSegment.image(
                        "file:///" + IMAGE_PATH + path + "/" + img_file
                    )
                else:
                    logger.warning(f"图片 {path}/{img_file} 不存在")
                    return MS.text("")
            else:
                return MessageSegment.image(img_file)

    @staticmethod
    def at(qq: Union[int, str]) -> MessageSegment:
        return MessageSegment.at(qq)

    @staticmethod
    def record(voice_name: str = "", path: Optional[str] = "") -> MessageSegment:
        if len(voice_name.split(".")) == 1:
            voice_name += ".mp3"
        if path == "":
            name = VOICE_PATH + "{}.".format(voice_name)
        else:
            name = VOICE_PATH + "{}/{}".format(path, voice_name)
        if voice_name.find("http") == -1:
            if os.path.exists(name):
                result = MessageSegment.record("file:///" + name)
                return result
            else:
                logger.warning(f"语音{path}/{voice_name} 不存在")
                return MS.text("")
        else:
            return MessageSegment.record(voice_name)

    @staticmethod
    def text(msg: str) -> MessageSegment:
        return MessageSegment.text(msg)

    @staticmethod
    def contact_user(qq: int) -> MessageSegment:
        return MessageSegment.contact_user(qq)

    @staticmethod
    def share(
        url: str = "",
        title: str = "",
        content: Optional[str] = None,
        image_url: Optional[str] = None,
    ) -> MessageSegment:
        return MessageSegment.share(url, title, content, image_url)

    @staticmethod
    def xml(data: str) -> MessageSegment:
        return MessageSegment.xml(data)

    @staticmethod
    def json(data: str) -> MessageSegment:
        data = ujson.dumps(data)
        return MessageSegment.json(data)

    @staticmethod
    def face(id_: int) -> MessageSegment:
        return MessageSegment.face(id_)

    @staticmethod
    def poke(id_: str) -> MessageSegment:
        return MessageSegment.poke("", id_)

    @staticmethod
    def music_163(id_: int) -> MessageSegment:
        return MessageSegment("music", {"type": "163", "id": id_})

    @staticmethod
    def reply(id_: int) -> MessageSegment:
        return MessageSegment.reply(id_)
