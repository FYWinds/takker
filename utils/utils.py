import time
import inspect
import warnings
import functools
from typing import List
from collections import defaultdict

import jionlp as jio
from nonebot.adapters import Event
from nonebot.adapters.cqhttp import Message

from utils.data import _time_definition
from db.utils.perm import Perm
from configs.config import HIDDEN_PLUGINS
from db.utils.plugin_manager import PluginManager


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


async def extract_mentioned_ids(message: Message) -> List[int]:
    """
    :说明: `extract_mentioned_ids`
    > 从消息中提取出所有被@的人的id

    :参数:
      * `message: Message`: 消息

    :返回:
      - `List[int]`: 被@的人的id列表
    """
    return [seg.data["qq"] for seg in message if seg.type == "at"]


async def extract_time_delta(message: Message) -> int:
    """
    :说明: `extract_time_delta`
    > 从消息内提取time_delta，返回秒级时间戳

    :参数:
      * `message: Message`: 消息

    :Exceptions:
      * `ValueError`: 未找到代表时间的语句

    :返回:
      - `int`: 秒级量度的时间戳
    """
    for seg in message:
        if seg.type == "text":
            cn_time = seg.data["text"]
    if not cn_time:
        raise ValueError("未找到代表时间的语句")
    try:
        _time = jio.parse_time(cn_time)
        if (
            _time.get("type", None) == "time_delta"
            and _time.get("definition", None) == "accurate"
        ):
            time_stamp: int = 0
            _time_time: dict[str, float] = _time["time"]
            for t in _time_time:
                time_stamp += int(_time_time[t]) * _time_definition[t]
            return time_stamp
        else:
            raise ValueError("未找到代表时间的语句")
    except (ValueError, KeyError):
        raise ValueError("未找到代表时间的语句")
