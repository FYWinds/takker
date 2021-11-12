from typing import List, Union

# 身份名单
OWNER: str = ""  # 主人
SUPERUSERS: List[Union[int, str]] = ["12345678", "0", "0", 12345678]  # 超级用户名单

# 各个API的配置
ALAPI_TOKEN: str = ""  # ALAPI
NETEASE_API: str = "nemapi.windis.xyz"  # NodeJS版本的网易云音乐API的地址
PIXIV_IMAGE_URL: str = "pixiv.windis.xyz"  # 反代i.pximg.net的网址
ALI_API_TOKEN: str = ""  # 阿里云市场API的APPcode 星座运势功能
WEATHER_API_KEY: str = ""  # 和风天气API key 天气功能

# 各种限制
MAX_PROCESS_TIME: int = 30  # 部分指令处理最大等待时间，单位秒，在此期间用户不能再次发起相同指令
BAN_CHEKC_FREQ: int = 5  # 恶意触发命令检测阈值
BAN_CHECK_PERIOD: int = 3  # 恶意触发命令检测时间
BAN_TIME: int = 5  # 恶意触发命令后的封禁时间，单位分钟

# 日志记录时长
DEBUG_LOG_TIME: int = 5  # 调试日志记录时长，单位天
INFO_LOG_TIME: int = 60  # 普通日志记录时长，单位天
ERROR_LOG_TIME: int = 90  # 错误日志记录时长，单位天

# 隐藏插件列表
HIDDEN_PLUGINS: List[str] = [
    "nonebot_plugin_apscheduler",
    "nonebot_plugin_test",
    "hooks",
    "invite_check",
    "withdraw",
]

# 数据自动备份
DB_BAKCUP_INTERVAL: int = 720  # 备份间隔，单位分钟
DB_BACKUP_COPIES: int = 12  # 保留的备份数量

WEATHER_DEFAULT: str = ""  # 天气插件默认城市/区

SUPERUSERS += list(map(int, SUPERUSERS))
SUPERUSERS = list(set(SUPERUSERS))
