import time
import inspect
import warnings
import functools
from typing import Union, Optional
from collections import defaultdict

from nonebot import require
from nonebot.adapters import Event

from db.utils.perm import Perm
from configs.config import HIDDEN_PLUGINS, MAX_PROCESS_TIME
from db.utils.plugin_manager import PluginManager

scheduler = require("nonebot_plugin_apscheduler").scheduler  # type: ignore


async def perm_check(perm: int, event: "Event") -> bool:
    """
    :说明:
        检查是否拥有足够权限等级

    :参数:
      * ``perm: int``: 权限等级
    """
    user_id = getattr(event, "user_id", None)
    group_id = getattr(event, "group_id", None)
    if group_id is not None and user_id is not None:
        u_perm = await Perm.check_perm(id=user_id, perm=perm)
        g_perm = await Perm.check_perm(id=group_id, perm=perm, isGroup=True)
        return u_perm or g_perm
    elif user_id is not None:
        u_perm = await Perm.check_perm(id=user_id, perm=perm)
        return u_perm
    return False


async def enable_check(plugin: str, event: "Event") -> bool:
    """
    :说明:
        检查插件是否开启

    :参数:
      * ``plugin: str``: 插件名
    """
    if plugin in HIDDEN_PLUGINS:
        return True
    user_id = getattr(event, "user_id", None)
    group_id = getattr(event, "group_id", None)
    if group_id is not None:
        p = await PluginManager.query_plugin_status(id=group_id, isGroup=True)
        return p[plugin]
    elif user_id is not None:
        p = await PluginManager.query_plugin_status(user_id)
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


def deprecated(reason: str):
    def decorator(func):
        if inspect.isclass(func):
            fmt = "Call to deprecated class {name}:{reason}"
        else:
            fmt = "Call to deprecated function {name}:{reason}"

        @functools.wraps(func)
        def _func(*args, **kwargs):
            warnings.warn(
                fmt.format(name=func.__name__, reason=reason),
                category=DeprecationWarning,
                stacklevel=2,
            )
            warnings.simplefilter("default", DeprecationWarning)
            return func(*args, **kwargs)

        return _func

    return decorator
