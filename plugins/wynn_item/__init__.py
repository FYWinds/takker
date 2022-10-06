import json
from pathlib import Path

import nonebot
from nonebot.plugin import on_command
from nonebot.typing import T_State
from thefuzz.process import extract as fuzzysearch
from nonebot.adapters.cqhttp import Bot, MessageEvent
from nonebot_plugin_apscheduler import scheduler

from utils.rule import limit_group
from utils.img_util import textToImageBuf
from utils.msg_util import image
from utils.text_util import align

__plugin_info__ = {
    "name": "Wynndata-Item",
    "des": "Wynncraft物品与素材数据查询",
    "usage": {
        "/wi <name>": "模糊搜索物品名",
    },
    "author": "风屿",
    "version": "1.5.0",
    "permission": 3,
}

driver = nonebot.get_driver()


wi = on_command(
    "/wi",
    aliases={".wi"},
    priority=20,
    block=True,
    rule=limit_group([521656488, 878663967, 211320297]),
)

with open("plugins/wynn_item/data/itemdb.json", "r", encoding="utf-8") as f:
    items: list[str] = json.load(f)

with open("plugins/wynn_item/data/ingre.json", "r", encoding="utf-8") as f:
    ingredients: list[str] = json.load(f)


@wi.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    name = str(event.message).strip()

    items_map = {i.lower(): i for i in items}
    ingredients_map = {i.lower(): i for i in ingredients}

    # 当直接打了全名时
    if name.lower() in items_map.keys():
        msg = str(
            Path(
                f"plugins/wynn_item/data/images/items/{items_map[name.lower()]}.png"
            ).absolute()
        )
    elif name.lower() in ingredients_map.keys():
        msg = str(
            Path(
                f"plugins/wynn_item/data/images/ingredients/{ingredients_map[name.lower()]}.png"
            ).absolute()
        )

    # 模糊搜索相似度前三的物品/素材
    else:
        probable_items = [i[0] for i in fuzzysearch(name, items, limit=3)]
        probable_ingredients = [i[0] for i in fuzzysearch(name, ingredients, limit=3)]

        state["pi"] = {_num: _name for _num, _name in enumerate(probable_items)}
        state["pg"] = {_num: _name for _num, _name in enumerate(probable_ingredients)}

        if not probable_ingredients and not probable_items:
            msg = "未找到物品"

        if len(probable_items) == 1 and not probable_ingredients:
            msg = msg = str(
                Path(
                    f"plugins/wynn_item/data/images/items/{probable_items[0]}.png"
                ).absolute()
            )
        elif len(probable_ingredients) == 1 and not probable_items:
            msg = msg = str(
                Path(
                    f"plugins/wynn_item/data/images/ingredients/{probable_ingredients[0]}.png"
                ).absolute()
            )

        else:
            newline = "\n"
            msg = f"""
您想查找的是
物品:
{newline.join(f"i{_num}. {_name}" for _num, _name in enumerate(probable_items)) if probable_items else ""}
材料:
{newline.join(f"g{_num}. {_name}" for _num, _name in enumerate(probable_ingredients)) if probable_ingredients else ""}
            """.strip()

    if msg.endswith(".png"):
        await wi.finish(image(abspath=msg))
    else:
        await bot.send(event, image(c=await textToImageBuf(msg, cut=0)))


@wi.got("answer")
async def _1(bot: Bot, event: MessageEvent, state: T_State):
    answer = str(state["answer"]).strip()
    if state["answer"].startswith("i"):
        try:
            name = state["pi"][int(answer[1:])]
            msg = str(Path(f"plugins/wynn_item/data/images/items/{name}.png").absolute())
        except IndexError:
            await wi.finish()
    elif state["answer"].startswith("g"):
        try:
            name = state["pg"][int(answer[1:])]
            msg = str(
                Path(f"plugins/wynn_item/data/images/ingredients/{name}.png").absolute()
            )
        except IndexError:
            await wi.finish()
    else:
        await wi.finish()

    await wi.finish(image(abspath=msg))
