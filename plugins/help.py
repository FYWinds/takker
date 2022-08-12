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

from utils.utils import enable_check
from db.utils.perm import Perm
from configs.config import HIDDEN_PLUGINS
from utils.img_util import textToImage
from utils.msg_util import at, image
from db.utils.plugin_perm import PluginPerm

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
            perm = await Perm.query_perm(id=str(event.group_id), isGroup=True)
        elif isinstance(event, PrivateMessageEvent):
            perm = await Perm.query_perm(id=str(event.user_id), isGroup=False)
        else:
            return
        for plugin in plugin_set:
            # 隐藏插件不显示在帮助菜单中
            if plugin.name in HIDDEN_PLUGINS:
                continue

            # 权限和插件开启判断，优先级 关闭状态>=权限>=开启状态
            enabled = await enable_check(plugin.name, event)
            try:
                plugin_perm = await PluginPerm.get_plugin_perm(plugin.name)
                assert plugin_perm is not None
            except AssertionError:
                plugin_perm = 5
            if (perm >= plugin_perm) and enabled:
                try:
                    plugin_name = getattr(plugin.module, "__plugin_name__", None)
                    assert plugin_name is not None
                    name = f"{plugin.name}: {plugin_name}"
                except AssertionError:
                    name = plugin.name
                try:
                    version = getattr(plugin.module, "__version__", None)
                    assert version is not None
                except AssertionError:
                    version = ""
                plugin_names.append(f"{name} {version} 权限:{plugin_perm}级")
        plugin_names.sort()
        newline_char = "\n"
        result = f"插件列表：\n{newline_char.join(plugin_names)}"
    else:
        try:
            plugin_name = state.get("content", None)
            assert plugin_name is not None
            plugin = nonebot.plugin.get_plugin(plugin_name)
        except AttributeError:
            plugin = None
        try:
            assert plugin is not None
            usage = getattr(plugin.module, "__usage__", None)
            assert usage is not None
            result = str("\n指令 | 说明" + "\n" + usage)
        except AssertionError:
            try:
                assert plugin is not None
                result = str(plugin.module.__doc__)
            except (AttributeError, AssertionError):
                result = f'{state.get("content")}插件不存在或未加载'
    await helper.finish(at(event.user_id) + image(c=(await textToImage(result))))


async def get_help():
    return """/help | 获取帮助菜单
/help list | 插件列表
/help <plugin_name> | 调取目标插件帮助信息
[必填] <可选参数> | 参数说明
"""
