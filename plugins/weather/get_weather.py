from httpx import AsyncClient

from configs.config import WEATHER_API_KEY

url_weather_api = "https://devapi.qweather.com/v7/weather/"
url_geoapi = "https://geoapi.qweather.com/v2/city/"

# 获取城市ID
async def get_Location(city_kw, api_type="lookup"):
    async with AsyncClient() as client:
        url = f"{url_geoapi}{api_type}?location={city_kw}&key={WEATHER_API_KEY}"
        res = await client.get(url)
        return res.json()


# 获取天气信息
async def get_WeatherInfo(api_type):
    async with AsyncClient() as client:
        url = f"{url_weather_api}{api_type}?location={city_id}&key={WEATHER_API_KEY}"
        res = await client.get(url)
        return res.json()


async def get_City_Weather(city):
    global city_id
    city_info = await get_Location(city)
    city_id = city_info["location"][0]["id"]
    city_name = city_info["location"][0]["name"]

    # 3天天气
    daily_info = await get_WeatherInfo("3d")
    daily = daily_info["daily"]
    day1 = daily[0]
    day2 = daily[1]
    day3 = daily[2]

    # 实时天气
    now_info = await get_WeatherInfo("now")
    now = now_info["now"]

    return {"city": city_name, "now": now, "day1": day1, "day2": day2, "day3": day3}
