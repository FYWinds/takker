import re

from nonebot import on_message
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import GROUP, Bot, GroupMessageEvent

__permission__ = 2

__plugin_name__ = "复读机"
__plugin_usage__ = """
被动插件，想要啥用法
"""
__plugin_author__ = "风屿"
__plugin_version__ = "1.0.0"

last_msg = {}
last_repeat_msg = {}
repeat_count = {}

repeater = on_message(permission=GROUP, priority=100, block=False)


@repeater.handle()
async def handle_repeater(bot: Bot, event: GroupMessageEvent, state: T_State):
    group_id = event.group_id

    global last_msg, last_repeat_msg, repeat_count

    try:
        last_msg[group_id]
    except KeyError:
        last_msg[group_id] = ""
    try:
        last_repeat_msg[group_id]
    except KeyError:
        last_repeat_msg[group_id] = ""

    t_msg = event.message
    msg = event.raw_message

    if re.match(r"^/", msg):
        return

    if msg != last_msg[group_id] or msg == last_repeat_msg[group_id]:
        last_msg[group_id] = msg
        repeat_count[group_id] = 0
        return
    else:
        repeat_count[group_id] += 1
        last_repeat_msg[group_id] = ""
        if repeat_count[group_id] >= 2:
            await repeater.send(t_msg)
            repeat_count[group_id] = 0
            last_msg[group_id] = ""
            last_repeat_msg[group_id] = msg
