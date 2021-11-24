import os
import time

import psutil
from nonebot import on_notice, on_command
from nonebot.rule import to_me
from nonebot.plugin import get_plugin
from nonebot.adapters.cqhttp import Bot, Message, MessageEvent, PokeNotifyEvent

from utils.data import process_time
from utils.rule import on_poke
from utils.browser import get_browser
from utils.msg_util import MS
from configs.path_config import TEMPLATE_PATH

__plugin_info__ = {
    "name": "机器人性能状态",
    "usage": {
        "戳一戳机器人": "返回性能状态",
        "@机器人 状态": "返回性能状态",
    },
    "author": "风屿",
    "version": "1.4.1",
    "permission": 1,
}


sp = on_notice(rule=on_poke() & to_me(), priority=20, block=False)
sc = on_command("状态", aliases={"当前状态"}, rule=to_me(), priority=20, block=False)


@sp.handle()
async def _sp(bot: Bot, event: PokeNotifyEvent):
    await sp.finish(await get_status())


@sc.handle()
async def _sc(bot: Bot, event: MessageEvent):
    await sc.finish(await get_status())


async def get_status() -> Message:
    plugin_list: dict[str, int] = {
        plugin: int(process_time[plugin].get_time() / 1e6) for plugin in process_time
    }
    plugin_list_cn: dict[str, int] = {}
    plugin_list = dict(
        sorted(plugin_list.items(), key=lambda item: item[1], reverse=True)
    )
    for k in plugin_list.keys():
        try:
            plugin = get_plugin(k)
            assert plugin is not None
            plugin_info = getattr(plugin.module, "__plugin_info__", {})
            plugin_name = plugin_info.get("name", plugin.name)
            plugin_list_cn[plugin_name] = plugin_list[k]
        except AssertionError:
            plugin_list_cn[k] = plugin_list[k]
    with open(f"{TEMPLATE_PATH}statistic/chart.html", "r", encoding="utf-8") as f:
        template = str(f.read())
    date = time.strftime("%Y-%m", time.localtime(time.time()))
    template = template.replace("[date]", date)
    template = template.replace("[plugin_list]", str(list(plugin_list_cn.keys())))
    template = template.replace("[times]", str(list(plugin_list_cn.values())))
    template = template.replace("群 [group-id] 本月插件调用统计", "Takker各插件指令处理时间一览")
    template = template.replace("调用次数", "处理时间(ms)")
    filename = "plugin_process_time_data"

    with open(
        f"{TEMPLATE_PATH}statistic/temp/{filename}.html", "w", encoding="utf-8"
    ) as f:
        f.write(template)

    pt_img = await generate_pic(filename)

    pid = os.getpid()
    cpu_percent = psutil.cpu_percent(interval=0.1)
    mem_percent = psutil.Process(pid).memory_percent()
    server_mem = psutil.virtual_memory().used / 1024 / 1024
    server_mem_percent = psutil.virtual_memory().percent
    total_mem = psutil.virtual_memory().total / 1024 / 1024
    message: str = f"""
CPU使用率: {cpu_percent:.2f}%
内存使用率: bot: {mem_percent:.2f}% | used: {server_mem_percent:.2f}%
bot: {mem_percent*total_mem/100:.2f} MB | used: {server_mem:.2f} MB | total: {total_mem:.2f} MB
"""
    return MS.text(message.strip()) + MS.image(c=pt_img)


async def generate_pic(filename: str):
    browser = await get_browser()
    page = await browser.new_page(device_scale_factor=2)
    await page.goto(f"file://{TEMPLATE_PATH}statistic/temp/{filename}.html")
    container = await page.query_selector("#container")
    assert container is not None
    img = await container.screenshot(type="png")
    await page.close()
    return img
