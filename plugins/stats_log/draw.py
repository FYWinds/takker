"""
Author: FYWindIsland
Date: 2021-08-20 17:05:54
LastEditTime: 2021-08-20 19:03:37
LastEditors: FYWindIsland
Description: 
I'm writing SHIT codes
"""
import time
from typing import List, Dict
from collections import Counter
from nonebot.plugin import get_plugin

from configs.path_config import TEMPLATE_PATH, IMAGE_PATH
from service.db.utils.statistic import query_illust_statue, query_status
from utils.browser import get_browser


async def draw_stat(group_id: int):
    with open(f"{TEMPLATE_PATH}statistic/chart.html", "r", encoding="utf-8") as f:
        template = str(f.read())
    p_stat = await query_status(group_id)
    p_list: Dict[str, int] = {}
    p_list_cn: Dict[str, int] = {}
    n_time = int(time.time() / 60 / 60 / 24)
    for day in range(n_time - 30, n_time + 1):
        day = str(day)
        if day in list(p_stat.keys()):
            p_list = dict(Counter(p_list) + Counter(p_stat[day]))
    for k in p_list.keys():
        try:
            plugin = get_plugin(k)
            assert plugin is not None
            plugin_name = plugin.module.__getattribute__("__plugin_name__")
            p_list_cn.update({plugin_name: p_list[k]})
        except:
            p_list_cn.update({k: p_list[k]})

    template = template.replace("[group-id]", str(group_id))
    date = time.strftime("%Y-%m", time.localtime(time.time()))
    template = template.replace("[date]", date)
    template = template.replace("[plugin_list]", str(list(p_list_cn.keys())))
    template = template.replace("[times]", str(list(p_list_cn.values())))

    filename = f"chart-{group_id}-normal"

    with open(
        f"{TEMPLATE_PATH}statistic/temp/{filename}.html",
        "w",
        encoding="utf-8",
    ) as f:
        f.write(template)

    await generate_pic(filename)
    return filename


async def draw_xp_stat(group_id: int):
    with open(f"{TEMPLATE_PATH}statistic/chart.html", "r", encoding="utf-8") as f:
        template = str(f.read())
    p_stat = await query_illust_statue(group_id)
    template = template.replace("本月插件调用统计", "xp统计")
    template = template.replace("[group-id]", str(group_id))
    date = time.strftime("%Y-%m", time.localtime(time.time()))
    template = template.replace("[date]", date)
    template = template.replace("[plugin_list]", str(list(p_stat.keys())))
    template = template.replace("[times]", str(list(p_stat.values())))

    filename = f"chart-{group_id}-xp"

    with open(
        f"{TEMPLATE_PATH}statistic/temp/{filename}.html",
        "w",
        encoding="utf-8",
    ) as f:
        f.write(template)

    await generate_pic(filename)
    return filename


async def generate_pic(filename: str):
    browser = await get_browser()
    page = await browser.new_page()
    await page.goto(f"file://{TEMPLATE_PATH}statistic/temp/{filename}.html")
    await page.set_viewport_size({"width": 1920, "height": 1080})
    container = await page.query_selector("#container")
    assert container is not None
    await container.screenshot(path=f"{IMAGE_PATH}statistic/{filename}.png")
