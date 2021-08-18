"""
Author: FYWindIsland
Date: 2021-08-12 09:36:34
LastEditTime: 2021-08-18 13:04:12
LastEditors: FYWindIsland
Description: 
I'm writing SHIT codes
"""
import time

from api.info import get_stranger_info

from service.db.utils.point import add_random_points
from .data_source import get_acg_image, get_stick
from configs.path_config import TEMPLATE_PATH, IMAGE_PATH
from utils.browser import get_browser


async def get_card(user_id: int):
    stick = await get_stick(user_id)
    acg_url = await get_acg_image()
    user_name = (await get_stranger_info(user_id))["nickname"]
    day_time = time.strftime("%m/%d", time.localtime())
    min_time = time.strftime("%H:%M", time.localtime())
    with open(f"{TEMPLATE_PATH}check_in/card2.html", "r", encoding="utf-8") as f:
        template = str(f.read())
    points = await add_random_points(user_id, 20)
    template = template.replace("static/", "../static/")
    template = template.replace("[acg_url]", acg_url)
    template = template.replace("[day_time]", day_time)
    # template = template.replace("[min_time]", min_time)
    template = template.replace("[user_name]", user_name)
    template = template.replace("[points]", str(points))
    template = template.replace("[luck-status]", stick["FORTUNE_SUMMARY"])
    template = template.replace("[star]", stick["LUCKY_STAR"])
    template = template.replace("[comment]", stick["SIGN_TEXT"])
    template = template.replace("[resolve]", stick["UN_SIGN_TEXT"])

    filename = f"card-{user_id}"
    with open(
        f"{TEMPLATE_PATH}check_in/temp/{filename}.html", "w", encoding="utf-8"
    ) as f:
        f.write(template)

    await generate_pic(filename)
    return f"{filename}.png"


async def generate_pic(filename: str):
    browser = await get_browser()
    page = await browser.new_page()
    await page.goto(f"file://{TEMPLATE_PATH}check_in/temp/{filename}.html")
    await page.set_viewport_size({"width": 1080, "height": 937})
    card = await page.query_selector("#card")
    assert card is not None
    await card.screenshot(path=f"{IMAGE_PATH}check_in/{filename}.png")
