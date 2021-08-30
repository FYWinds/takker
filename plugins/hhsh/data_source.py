import httpx

from utils.browser import get_ua


async def get_sx(word: str) -> str:
    url = "https://lab.magiconch.com/api/nbnhhsh/guess"
    data = {"text": word}

    async with httpx.AsyncClient(headers=get_ua()) as client:
        resp = await client.post(url=url, data=data)
    resp = resp.json()
    try:
        result = f"查询到缩写 {word} 代表的实际内容:\n"
        result += ", ".join(resp[0]["trans"])
    except:
        result = f"未查询到相关缩写"
    return result
