import httpx
from rcon import rcon
from nonebot.plugin import on_notice, on_command
from nonebot.adapters.cqhttp import Bot, MessageEvent, GroupUploadNoticeEvent

from utils.browser import get_ua
from configs.config import MC_PATH, SPECIAL_IP, SUPERUSERS, SPECIAL_PASS

__permission__ = 9
__plugin_name__ = "远程执行mc指令-jpgnl专用"
__usage__ = "sudo <指令>"

command = on_command("sudo", priority=20)


@command.handle()
async def _(bot: Bot, event: MessageEvent):
    if (
        not event.sender.role in ["admin", "owner"]
        and str(event.sender.user_id) not in SUPERUSERS
    ):
        return
    c = event.get_plaintext().strip()
    result = await rcon(c, host=SPECIAL_IP, port=25575, passwd=SPECIAL_PASS)
    await format(result)
    await command.finish(result)


async def format(text: str) -> str:
    CHAR = "\u00A7"  # §
    NAME_MAP = {
        "black": "0",
        "dark_blue": "1",
        "dark_green": "2",
        "dark_aqua": "3",
        "dark_red": "4",
        "dark_purple": "5",
        "gold": "6",
        "gray": "7",
        "dark_gray": "8",
        "blue": "9",
        "green": "a",
        "aqua": "b",
        "red": "c",
        "light_purple": "d",
        "yellow": "e",
        "white": "f",
        "obfuscated": "k",
        "bold": "l",
        "strikethrough": "m",
        "underlined": "n",
        "italic": "o",
    }
    index = 0
    while index < len(text) - 1 and type(text) == str:
        if text[index] == CHAR:
            form = text[index + 1]
            if form in NAME_MAP:
                text = text.replace(CHAR + form, "")
                index = index - 1
                continue
        index = index + 1
    return text


schem = on_notice(priority=20)


@schem.handle()
async def _s(bot: Bot, event: GroupUploadNoticeEvent):
    if event.group_id != 669041320 and event.group_id != 521656488:
        return
    if ".schematic" not in event.file.name:
        return
    try:
        url = event.dict()["file"]["url"]
    except:
        return
    if url:
        async with httpx.AsyncClient(headers=get_ua()) as client:
            f = await client.get(url)
        with open(f"{MC_PATH}/{event.file.name}", "wb") as file:
            file.write(f.content)
