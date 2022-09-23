import httpx

BASE_URL: str = "https://wynn.windis.cn"
ENDPOINT: str = "/public_api.php"

aclient = httpx.AsyncClient


async def get_player_info(name: str) -> dict:
    url = f"{BASE_URL}/v2/player/{name}/stats"
    async with aclient() as client:
        r = await client.get(url)
    return r.json()


async def get_player_info_v3(name: str) -> dict:
    url = f"https://wynn.windis.cn/v3/player/{name}"
    async with aclient() as client:
        r = await client.get(url)
    return r.json()


async def get_player_uuid(name: str) -> dict:
    url = f"{BASE_URL}/v2/player/{name}/uuid"
    async with aclient() as client:
        r = await client.get(url)
    return r.json()


async def search_item(name: str) -> dict:
    url = f"{BASE_URL}{ENDPOINT}"
    params = {
        "action": "itemDB",
        "search": name,
    }
    async with aclient() as client:
        r = await client.get(url, params=params)
    return r.json()


async def get_servers() -> dict:
    url = f"{BASE_URL}{ENDPOINT}"
    params = {"action": "onlinePlayers"}
    async with aclient() as client:
        r = await client.get(url, params=params)
    return r.json()
