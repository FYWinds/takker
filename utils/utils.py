# 该文件部分内容参考了HibiKier/zhenxun_bot
import time
from collections import defaultdict

from nonebot import require
from nonebot.adapters.cqhttp import Event, GroupMessageEvent, PrivateMessageEvent

from configs.config import MAX_PROCESS_TIME
from service.db.utils.perm import check_perm
from service.db.utils.plugin_manager import query_plugin_status


scheduler = require("nonebot_plugin_apscheduler").scheduler  # type: ignore


async def perm_check(perm: int, event: "Event") -> bool:
    """
    :说明:
        检查是否拥有足够权限等级(仅支持cqhttp)

    :参数:
      * ``perm: int``: 权限等级
    """
    if isinstance(event, GroupMessageEvent):
        u_perm = await check_perm(id=str(event.user_id), perm=perm)
        g_perm = await check_perm(id=str(event.group_id), perm=perm, isGroup=True)
        return u_perm or g_perm
    elif isinstance(event, PrivateMessageEvent):
        u_perm = await check_perm(id=str(event.user_id), perm=perm)
        return u_perm
    return False


async def enable_check(plugin: str, event: "Event") -> bool:
    """
    :说明:
        检查插件是否开启

    :参数:
      * ``plugin: str``: 插件名
    """
    if isinstance(event, GroupMessageEvent):
        p = await query_plugin_status(id=str(event.group_id), isGroup=True)
        return p[plugin]
    elif isinstance(event, PrivateMessageEvent):
        p = await query_plugin_status(str(event.user_id))
        return p[plugin]
    return False


class Processing:
    """
    :说明:
    > 限制用户在处理期间重复使用指令
    """

    def __init__(self):
        self.processing = defaultdict(bool)
        self.time = time.time()

    def set_True(self, key):
        self.time = time.time()
        self.processing[key] = True

    def set_False(self, key):

        self.processing[key] = False

    def check(self, key):
        if time.time() - self.time > MAX_PROCESS_TIME:
            self.set_False(key)
            return False
        return self.processing[key]


class FreqLimiter:
    """
    :说明:
    > 命令CD
    """

    def __init__(self, cd):
        self.end_time = defaultdict(float)
        self.cd = cd

    def check(self, key) -> bool:
        return time.time() >= self.end_time[key]

    def start_cd(self, key, cd=0):
        self.end_time[key] = time.time() + (cd if cd > 0 else self.cd)

    def left_time(self, key) -> float:
        return self.end_time[key] - time.time()


class ExploitCheck:
    """
    :说明: ``
    > 滥用检测
    """

    def __init__(self, default_check_time: float = 5, default_count: int = 4):
        self.mint = defaultdict(int)
        self.mtime = defaultdict(float)
        self.check_time = default_check_time
        self.count = default_count

    def add(self, key):
        if self.mint[key] == 1:
            self.mtime[key] = time.time()
        self.mint[key] += 1

    def check(self, key) -> bool:
        if time.time() - self.mtime[key] > self.check_time:
            self.mtime[key] = time.time()
            self.mint[key] = 0
            return False
        if (
            self.mint[key] >= self.count
            and time.time() - self.mtime[key] < self.check_time
        ):
            self.mtime[key] = time.time()
            self.mint[key] = 0
            return True
        return False
