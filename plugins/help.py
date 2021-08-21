"""
Author: FYWindIsland
Date: 2021-08-13 13:57:24
LastEditTime: 2021-08-21 15:19:23
LastEditors: FYWindIsland
Description: 
I'm writing SHIT codes
"""
import nonebot
import nonebot.plugin
from nonebot import on_command
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import (
    Bot,
    Event,
    MessageEvent,
    GroupMessageEvent,
    PrivateMessageEvent,
)

from service.db.utils.perm import query_perm
from utils.utils import enable_check
from utils.msg_util import at, text
from configs.config import HIDDEN_PLUGINS

__usage__ = """/help | 获取帮助菜单
/help list | 插件列表
/help <plugin_name> | 调取目标插件帮助信息
[必填] <可选参数> | 参数说明
"""

__plugin_name__ = "帮助菜单"

__permission__ = 0

helper = on_command("/help", priority=20)


@helper.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    args = str(event.get_message()).strip()
    if args:
        state["content"] = args
    else:
        state["content"] = ""


@helper.got("content")
async def get_result(bot: Bot, event: MessageEvent, state: T_State):
    if not state.get("content"):
        result = await get_help()
    elif str(state.get("content")).lower() == "list":
        plugin_set = nonebot.plugin.get_loaded_plugins()
        plugin_names = []
        if isinstance(event, GroupMessageEvent):
            perm = await query_perm(id=str(event.group_id), isGroup=True)
        elif isinstance(event, PrivateMessageEvent):
            perm = await query_perm(id=str(event.user_id), isGroup=False)
        else:
            return
        for plugin in plugin_set:
            if plugin.name in HIDDEN_PLUGINS:
                continue
            enabled = await enable_check(plugin.name, event)
            try:
                plugin_perm = plugin.module.__getattribute__("__permission__")
            except:
                plugin_perm = 5
            if perm >= plugin_perm and enabled:
                try:
                    name = f'{plugin.name}: {plugin.module.__getattribute__("__plugin_name__")}'
                except:
                    name = plugin.name
                try:
                    version = plugin.module.__getattribute__("__version__")
                except:
                    version = ""
                plugin_names.append(f"{name} {version} 权限:{plugin_perm}级")
        plugin_names.sort()
        newline_char = "\n"
        result = f"插件列表：\n{newline_char.join(plugin_names)}"
    else:
        try:
            plugin = nonebot.plugin.get_plugin(state.get("content"))  # type: ignore
        except AttributeError:
            plugin = None
        try:
            result = "\n指令 | 说明" + "\n" + plugin.module.__getattribute__("__usage__")  # type: ignore
        except:
            try:
                result = plugin.module.__doc__  # type: ignore
            except AttributeError:
                result = f'{state.get("content")}插件不存在或未加载'
    await helper.finish(at(event.user_id) + text(result))


async def get_help():
    return """/help | 获取帮助菜单
/help list | 插件列表
/help <plugin_name> | 调取目标插件帮助信息
[必填] <可选参数> | 参数说明
"""
