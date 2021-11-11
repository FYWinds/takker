import time
from typing import Optional

from nonebot.log import logger
from nonebot.typing import T_State
from nonebot.matcher import Matcher
from nonebot.message import run_preprocessor, run_postprocessor
from nonebot.adapters import Bot, Event

from utils.data import ProcessTime, process_time
from configs.config import HIDDEN_PLUGINS


@run_preprocessor
async def start_time_log(matcher: Matcher, bot: Bot, event: Event, state: T_State):
    state["start_time"] = time.time_ns()  # 以纳秒为单位记录开始处理的时间
    state["plugin_name"] = (
        matcher.plugin_name if matcher.plugin_name not in HIDDEN_PLUGINS else "Inner."
    )


@run_postprocessor
async def end_time_log(
    matcher: Matcher, e: Optional[Exception], bot: Bot, event: Event, state: T_State
):
    global process_time
    if "start_time" not in state:
        return
    if state.get("_prefix", {}).get("raw_command", None) is None:
        return
    start_time = state["start_time"]
    plugin_name = state.get("plugin_name", "Unknown")
    end_time = time.time_ns()
    logger.debug(f"{plugin_name} took {(end_time - start_time) / 1e6:.2f}ms")
    if plugin_name in process_time:
        process_time[plugin_name].add_time(end_time - start_time)
    else:
        process_time[plugin_name] = ProcessTime(plugin_name, end_time - start_time)
