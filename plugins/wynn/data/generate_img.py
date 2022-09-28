import os
import json
from typing import Optional

import anyio
from playwright.async_api import Browser, TimeoutError, async_playwright

_browser: Optional[Browser] = None
BASE_URL = "https://www.wynndata.tk/i/"


async def init(**kwargs) -> Browser:
    global _browser
    browser = await async_playwright().start()
    _browser = await browser.chromium.launch(**kwargs)
    return _browser


async def get_browser(**kwargs) -> Browser:
    return _browser or await init(**kwargs)


async def close_browser():
    if _browser:
        await _browser.close()


async def gen_image(name: str, type: str) -> None:
    try:
        browser = await get_browser()
        page = await browser.new_page(device_scale_factor=2)
        await page.goto(f"{BASE_URL}{name}")
        await page.evaluate(
            'document.querySelector("body > div.container-fluid.dirt-bg > div > div > div.col-xs-12.col-md-8 > div.cb-success-big.shareable_url_new.shareable_url_new__big").style.display = "none"'
        )
        if type == "items":
            await page.evaluate(
                'document.querySelector("body > div.container-fluid.dirt-bg > div > div.row > div.col-xs-12.col-md-8 > div.ci-buttons").style.display = "none"'
            )
        card = await page.query_selector(
            "body > div.container-fluid.dirt-bg > div > div.row"
        )
        assert card is not None
        img = await card.screenshot(type="png")
        await page.close()
        with open(f"./images/{type}/{name}.png", "wb") as f:
            f.write(img)
    except TimeoutError:
        await gen_image(name, type)


async def check_image(name: str, type: str) -> bool:
    if f"{name}.png" in os.listdir(f"./images/{type}/"):
        return True
    return False


async def gen_all_image() -> None:
    with open("ingre.json", "r", encoding="utf-8") as f:
        ingredients = json.load(f)
    with open("itemdb.json", "r", encoding="utf-8") as f:
        items = json.load(f)
    done = 0
    num = len(items["items"])
    for item in items["items"]:
        if not await check_image(item["name"], "items"):
            await gen_image(item["name"], "items")
        done += 1
        print(f"\r物品生成 [{done}/{num}]")
    print("物品图片生成完毕")
    done = 0
    num = len(ingredients)
    for ingredient in ingredients:
        if not await check_image(ingredient, "ingredients"):
            await gen_image(ingredient, "ingredients")
        print(f"\r素材生成 [{done}/{num}]")
    print("素材图片生成完毕")
    await close_browser()


if __name__ == "__main__":
    anyio.run(gen_all_image)
