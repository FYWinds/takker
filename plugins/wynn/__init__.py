import datetime

import nonebot
from nonebot.plugin import on_shell_command
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import Bot, MessageEvent
from nonebot_plugin_apscheduler import scheduler

from utils.rule import limit_group
from utils.img_util import textToImageBuf
from utils.msg_util import image

from .parser import wynn_parser
from .data_source import get_servers
from .data_storage import get_data, set_data, save_data

__plugin_info__ = {
    "name": "Wynndata",
    "des": "Wynncraft玩家数据查询",
    "usage": {
        "/wynn bind <id>": "绑定自己游戏ID",
        "/wynn stats [id] [-v/--verbose]": "查询指定ID的数据，省略则为查询已绑定ID的数据 -v: 更详细的数据",
        # "/wynn item <name1> [name2] ... [-v/--verbose]": "查询物品信息 -v: 更详细的数据",
        "/wynn uptime [server1] [server2] ... [-sp/--soulpoint]": "查询服务器开启时间 -sp: 按照灵魂点恢复排序",
        ".wi <name>": "模糊搜索物品/素材信息",
    },
    "author": "风屿",
    "version": "1.5.0",
    "permission": 3,
}

driver = nonebot.get_driver()


@driver.on_bot_disconnect  # type: ignore
async def save(bot: Bot):
    save_data(get_data())


wynn = on_shell_command(
    "/wynn",
    parser=wynn_parser,
    priority=1,
    block=True,
    rule=limit_group([211320297, 521656488, 878663967]),
)


@wynn.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    args = state["args"]
    args.uid = str(event.user_id)

    if hasattr(args, "handle"):
        message: str = await args.handle(args)
        if message:
            if message.find("错误:") == -1:
                await bot.send(event, image(c=await textToImageBuf(message, cut=0)))
            else:
                await bot.send(event, message=message)


@scheduler.scheduled_job("interval", seconds=10, id="wynn_get_uptime")
async def get_uptime():
    data = get_data()
    server_list = await get_servers()
    for s in server_list:
        if s == "request":
            continue
        if s not in data["servers"]:
            data["servers"][s] = {
                "online": False,
                "timestarted": "",
                "playerscount": -1,
                "players": [],
            }
        if not data["servers"][s]["online"]:
            data["servers"][s]["timestarted"] = datetime.datetime.now().isoformat()
        data["servers"][s]["online"] = True
        data["servers"][s]["playerscount"] = len(server_list[s])
        data["servers"][s]["players"] = server_list[s]
    for s in data["servers"]:
        if s not in server_list:
            data["servers"][s]["online"] = False
    data["servers"] = {s: data["servers"][s] for s in sorted(data["servers"])}
    set_data(data)
