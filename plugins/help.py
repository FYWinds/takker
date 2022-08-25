from typing import Union

import nonebot.plugin
from nonebot import on_command
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import (
    Bot,
    MessageEvent,
    GroupMessageEvent,
    PrivateMessageEvent,
)

from utils.utils import enable_check
from db.utils.perm import Perm
from configs.config import OWNER, SUPERUSERS, HIDDEN_PLUGINS
from utils.img_util import textToImage
from utils.msg_util import at, image
from utils.text_util import align
from db.utils.plugin_perm import PluginPerm

__plugin_info__: dict[
    str, Union[str, dict[str, Union[dict[str, Union[int, str]], str]], int]
] = {
    "name": "帮助菜单",
    "des": "查看各个插件的帮助菜单",
    "usage": {
        "/help": "获取帮助菜单",
        "/help <插件名>": {"des": "获取指定插件的帮助菜单", "eg": "/help bili_sub"},
        "/help list": "获取能查看帮助的插件列表",
    },
    "author": "风屿",
    "version": "1.4.0",
    "permission": 0,
}

helper = on_command("/help", priority=20)


@helper.handle()
async def handle_first_receive(bot: Bot, event: MessageEvent, state: T_State):
    args = str(event.get_message()).strip()
    if args:
        state["content"] = args
    else:
        state["content"] = ""


@helper.got("content")
async def get_result(bot: Bot, event: MessageEvent, state: T_State):
    if str(state.get("content")).lower() == "list":
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
            plugin_perm = await PluginPerm.get_plugin_perm(plugin.name)
            if (perm >= plugin_perm) and enabled:
                plugin_info: dict = getattr(plugin.module, "__plugin_info__", {})
                plugin_name = plugin_info.get("name", "未命名")
                version = plugin_info.get("version", "未知")
                info = f"{align(plugin.name, 18)}: {align(plugin_name+ ' '+version, 32)}"
                plugin_names.append(f"{info} 权限:{align(plugin_perm, 2)}级")
        plugin_names.sort()
        newline_char = "\n"
        message = f"插件列表：\n{newline_char.join(plugin_names)}"
        await helper.finish(
            at(event.user_id) + image(c=(await textToImage(message.strip())))
        )
    else:
        if event.user_id in SUPERUSERS or str(event.user_id) == OWNER:
            identity = "superuser"
        elif event.sender.role in ["admin", "owner"]:
            identity = "owner"
        else:
            identity = "norm"
        try:
            plugin_name = state.get("content", None)
            if not plugin_name:
                plugin_name = "help"
            plugin = nonebot.plugin.get_plugin(plugin_name)
        except AttributeError:
            plugin_name = ""
            plugin = None
        try:
            assert plugin is not None
            plugin_info: dict = getattr(plugin.module, "__plugin_info__", {})
            if plugin_info:
                message = await build_message(plugin_info, identity)
                doc = plugin_info.get("doc", "暂无文档")
            else:
                message = "暂无信息"
                doc = "暂无文档"
            await helper.finish(
                at(event.user_id)
                + image(c=(await textToImage(message.strip(), 96)))
                + f"文档地址: {doc}"
            )
        except (AttributeError, AssertionError):
            await helper.finish(at(event.user_id) + f'{state.get("content")}插件不存在或未加载')


async def build_message(plugin_info: dict, identity: str = "norm") -> str:
    message = f"""
插件: {plugin_info.get("name", "未命名")}
作者: {plugin_info.get("author", "未知")}
权限: {plugin_info.get("permission", 0)} 级
版本: {plugin_info.get("version", "未知")}
介绍: {plugin_info.get("des", "无简介")}
""".strip()
    usage: dict[str, dict[str, str]] = plugin_info.get("usage", {})
    admin_usage: dict[str, dict[str, str]] = plugin_info.get("admin_usage", {})
    superuser_usage: dict[str, dict[str, str]] = plugin_info.get("superuser_usage", {})
    if identity == "norm":
        if usage:
            message += "\n \n指令列表:"
            message = await add_usage(message, usage)
    elif identity == "admin":
        if usage:
            message += "\n \n指令列表:"
            message = await add_usage(message, usage)
        if admin_usage:
            message += "\n \n管理员指令列表:"
            message = await add_usage(message, admin_usage)
    elif identity == "superuser":
        if usage:
            message += "\n \n指令列表:"
            message = await add_usage(message, usage)
        if admin_usage:
            message += "\n \n管理员指令列表:"
            message = await add_usage(message, admin_usage)
        if superuser_usage:
            message += "\n \n超级管理员指令列表:"
            message = await add_usage(message, superuser_usage)
    addition_info = plugin_info.get("additional_info", "")
    message += f"\n \n{addition_info}"
    return message


async def add_usage(message: str, usage: dict) -> str:
    blank = " " * 4
    if usage:
        for key, value in usage.items():
            if isinstance(value, dict):
                if value.get("des"):
                    message += f"\n{blank}{align(key, 32)}| {value['des']}"
                else:
                    message += f"\n{blank}{align(key, 32)}| 无说明"
                if value.get("eg"):
                    message += f"\n{blank}{blank}示例: {value['eg']}"
            else:
                message += f"\n{blank}{align(key, 32)}| {value}"
    return message
