import os
import re
import json
import random

import jieba
import jieba.analyse

from configs.path_config import TEXT_PATH, VOICE_PATH

a = """{"petpet": true, "kisskiss": true}"""

print(
    list(
        {
            "send_tags": True,  # 是否发送tags
            "send_image": True,  # 是否发送图片
            "send_author": True,  # 是否发送作者和uid
            "send_name": True,  # 是否发送图片名字
            "send_link": True,  # 是否发送原图链接
        }.keys()
    )
)
