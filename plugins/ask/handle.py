"""
Author: FYWindIsland
Date: 2021-08-14 21:34:31
LastEditTime: 2021-08-24 11:51:07
LastEditors: FYWindIsland
Description: 
I'm writing SHIT codes
"""
import re
import random
import asyncio
from typing import List

from api.info import get_group_member_list


async def how_many(message: str) -> str:
    while re.findall("几|多少", message):
        message = message.replace("几", str(random.randint(0, 99)), 1)
        message = message.replace("多少", str(random.randint(0, 99)), 1)
    return message


async def what_time(message: str) -> str:
    time = ["早上", "中午", "晚上", "今天", "明天", "下周", "下个月", "明年"]
    while re.findall("什么时候|啥时候", message):
        message = message.replace("什么时候", random.choice(time), 1)
        message = message.replace("啥时候", random.choice(time), 1)
    return message


async def how_long(message: str) -> str:
    unit = ["秒", "小时", "天", "周", "月", "年", "世纪"]
    while re.findall("多久|多长时间", message):
        message = message.replace(
            "多久", str(random.randint(0, 99)) + random.choice(unit), 1
        )
        message = message.replace(
            "多长时间", str(random.randint(0, 99)) + random.choice(unit), 1
        )
    return message


async def hif(message: str) -> str:
    keyword = list(set(re.findall("(.)不\1", message)))
    for k in keyword:
        if random.choice([True, False]):
            message = message.replace(k, k[:1])
        else:
            message = message.replace(k, k[1:])
    return message


async def who(message: str, group_id: int) -> str:
    group_member_list = await get_group_member_list(group_id)
    member_list: List[str] = []
    for n in group_member_list:
        member_list += [n["nickname"]]
    while "谁" in message:
        member_name = member_list[random.randint(0, len(member_list)) - 1]
        message = message.replace("谁", member_name, 1)
    return message


async def handle_pers(message: str) -> str:
    message_list = list(message)
    for i in range(0, len(message_list)):
        if message_list[i] == "我":
            message_list[i] = "你"
            continue
        if message[i] == "你":
            message_list[i] = "我"
            continue

    message = "".join(message_list)

    message = message.replace("bot", "我")
    message = message.replace("Bot", "我")
    message = message.replace("吗", "")
    message = message.replace("呢", "")
    message = message.replace("？", "")
    message = message.replace("?", "")

    return message
