"""
Author: FYWindIsland
Date: 2021-08-01 07:48:46
LastEditTime: 2021-08-12 09:42:08
LastEditors: FYWindIsland
Description: Takker的各项配置所在之处
I'm writing SHIT codes
"""
from typing import List, Union

# Go-cq正向http地址配置(默认使用bot.call_api()的调用方式)
USE_HTTP_API: bool = False
CQ_HTTP_URL: str = "http://127.0.0.1:5701"
CQ_SECRET: str = ""  # HTTP_API的secret

# 超级用户名单
SUPERUSERS: List[str] = ["0", "2330705135"]

# 各个API的Token
ALAPI_TOKEN: str = "F71XeXpJSBzIjIim"

# 各种限制
MAX_PROCESS_TIME: int = 30  # 部分指令处理最大等待时间，单位秒，在此期间用户不能再次发起相同指令
BAN_CHEKC_FREQ: int = 5  # 恶意触发命令检测阈值
BAN_CHECK_PERIOD: int = 3  # 恶意触发命令检测时间
BAN_TIME: int = 5  # 恶意触发命令后的封禁时间，单位分钟

# 隐藏插件列表
HIDDEN_PLUGINS: List[str] = ["nonebot_plugin_apscheduler", "hook"]
