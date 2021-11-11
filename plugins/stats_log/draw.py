import time
from collections import Counter

from nonebot.plugin import get_plugin

from utils.browser import get_browser
from configs.path_config import TEMPLATE_PATH
from db.models.statistic import Statistic


async def draw_stat(group_id: int):
    with open(f"{TEMPLATE_PATH}statistic/chart.html", "r", encoding="utf-8") as f:
        template = str(f.read())
    p_stat = await Statistic.query_status(group_id)
    p_list: dict[str, int] = {}
    p_list_cn: dict[str, int] = {}
    n_time = int(time.time() / 60 / 60 / 24)
    for day in range(n_time - 30, n_time + 1):
        day = str(day)
        if day in list(p_stat.keys()):
            p_list = dict(Counter(p_list) + Counter(p_stat[day]))
    p_list = dict(sorted(p_list.items(), key=lambda item: item[1], reverse=True))
    for k in p_list.keys():
        try:
            plugin = get_plugin(k)
            assert plugin is not None
            plugin_info = getattr(plugin.module, "__plugin_info__", {})
            plugin_name = plugin_info.get("name", plugin.name)
            p_list_cn |= {plugin_name: p_list[k]}
        except AssertionError:
            p_list_cn |= {k: p_list[k]}
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

    return await generate_pic(filename)


async def draw_xp_stat(group_id: int):
    with open(f"{TEMPLATE_PATH}statistic/chart.html", "r", encoding="utf-8") as f:
        template = str(f.read())
    p_stat = await Statistic.query_illust_statue(group_id)
    p_stat_sorted = dict(sorted(p_stat.items(), key=lambda item: item[1], reverse=True))
    p_stat_final: dict[str, int] = {}
    for i in range(0, 7):
        try:
            key = list(p_stat_sorted.keys())[i]
            p_stat_final |= {key: p_stat_sorted[key]}
        except IndexError:
            break
    template = template.replace("本月插件调用统计", "xp统计")
    template = template.replace("[group-id]", str(group_id))
    date = time.strftime("%Y-%m", time.localtime(time.time()))
    template = template.replace("[date]", date)
    template = template.replace("[plugin_list]", str(list(p_stat_final.keys())))
    template = template.replace("[times]", str(list(p_stat_final.values())))

    filename = f"chart-{group_id}-xp"

    with open(
        f"{TEMPLATE_PATH}statistic/temp/{filename}.html",
        "w",
        encoding="utf-8",
    ) as f:
        f.write(template)

    return await generate_pic(filename)


async def generate_pic(filename: str):
    browser = await get_browser()
    page = await browser.new_page(device_scale_factor=2)
    await page.goto(f"file://{TEMPLATE_PATH}statistic/temp/{filename}.html")
    container = await page.query_selector("#container")
    assert container is not None
    img = await container.screenshot(type="png")
    await page.close()
    return img
