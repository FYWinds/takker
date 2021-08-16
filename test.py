"""
Author: FYWindIsland
Date: 2021-08-10 19:17:29
LastEditTime: 2021-08-15 15:22:12
LastEditors: FYWindIsland
Description: 
I'm writing SHIT codes
"""
import re
import random

message = str("行不行行不行能不能是不是可不可以行不行")
text = list(set(re.findall(".?不.?", message)))

print(bool(message.find("行")))


def hif(message: str) -> str:
    keyword = list(set(re.findall(".?不.?", message)))
    for k in keyword:
        if random.choice([True, False]):
            message = message.replace(k, k[:1])
        else:
            message = message.replace(k, k[1:])
    return message


async def how_many(message: str) -> str:
    while message.find("几"):
        message = message.replace("几", str(random.randint(0, 99)), 1)
    while message.find("多少"):
        message = message.replace("多少", str(random.randint(0, 99)), 1)
    return message


async def what_time(message: str) -> str:
    time = ["早上", "中午", "晚上", "今天", "明天", "下周", "下个月", "明年"]
    while message.find("什么时候"):
        message = message.replace("什么时候", random.choice(time), 1)
    while message.find("啥时候"):
        message = message.replace("啥时候", random.choice(time), 1)
    return message


async def how_long(message: str) -> str:
    unit = ["秒", "小时", "天", "周", "月", "年", "世纪"]
    while message.find("多久"):
        message = message.replace(
            "多久", str(random.randint(0, 99)) + random.choice(unit), 1
        )
    while message.find("多长时间"):
        message = message.replace(
            "多长时间", str(random.randint(0, 99)) + random.choice(unit), 1
        )
    return message


print(hif(message))
