"""
Author: FYWindIsland
Date: 2021-08-14 16:12:07
LastEditTime: 2021-08-14 16:18:59
LastEditors: FYWindIsland
Description: 
I'm writing SHIT codes
"""
import httpx

from utils.user_agent import get_ua


async def get_sx(word: str) -> str:
    url = "https://lab.magiconch.com/api/nbnhhsh/guess"
    data = {"text": word}

    async with httpx.AsyncClient(headers=get_ua()) as client:
        resp = await client.post(url=url, data=data)
    resp = resp.json()
    try:
        result = f"查询到缩写 {word} 代表的实际内容:\n"
        for trans in resp[0]["trans"]:
            result += trans
    except:
        result = f"未查询到相关缩写"
    return result
