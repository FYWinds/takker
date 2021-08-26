from typing import List

# Go-cq正向http地址配置(默认使用bot.call_api()的调用方式)
USE_HTTP_API: bool = False
CQ_HTTP_URL: str = ""
CQ_SECRET: str = ""  # HTTP_API的secret

# 身份名单
OWNER: str = ""  # 主人
SUPERUSERS: List[str] = ["0", "", ""]  # 超级用户名单

# 各个API的配置
ALAPI_TOKEN: str = ""  # ALAPI
CATAPI_TOKEN: str = ""  # 随机猫猫API
NETEASE_API: str = "nemapi.windis.xyz"  # NodeJS版本的网易云音乐API的地址
PIXIV_IMAGE_URL: str = "pixiv.windis.xyz"  # 反代i.pximg.net的网址

# 各种限制
MAX_PROCESS_TIME: int = 30  # 部分指令处理最大等待时间，单位秒，在此期间用户不能再次发起相同指令
BAN_CHEKC_FREQ: int = 5  # 恶意触发命令检测阈值
BAN_CHECK_PERIOD: int = 3  # 恶意触发命令检测时间
BAN_TIME: int = 5  # 恶意触发命令后的封禁时间，单位分钟

# 隐藏插件列表
HIDDEN_PLUGINS: List[str] = [
    "nonebot_plugin_apscheduler",
    "nonebot_plugin_test",
    "hook",
    "invite_check",
    "withdraw",
]
