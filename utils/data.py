"""
Author: FYWindIsland
Date: 2021-08-12 10:40:00
LastEditTime: 2021-08-12 11:03:13
LastEditors: FYWindIsland
Description: 
I'm writing SHIT codes
"""
import json

from nonebot.log import logger

from configs.path_config import TEXT_PATH


fortune: dict
msg_of_day: dict

with open(f"{TEXT_PATH}fortune.json", "r", encoding="utf-8") as file:
    fortune = json.load(file)["data"]

with open(f"{TEXT_PATH}msg_of_day.json", "r", encoding="utf-8") as file:
    msg_of_day = json.load(file)["data"]
