import json

from nonebot.log import logger

from configs.path_config import TEXT_PATH


fortune: list[dict]
msg_of_day: list[dict]
atri_text: list[dict]

with open(f"{TEXT_PATH}fortune.json", "r", encoding="utf-8") as file:
    fortune = json.load(file)["data"]

with open(f"{TEXT_PATH}msg_of_day.json", "r", encoding="utf-8") as file:
    msg_of_day = json.load(file)["data"]

with open(f"{TEXT_PATH}atri.json", "r", encoding="utf-8") as file:
    atri_text = json.load(file)
