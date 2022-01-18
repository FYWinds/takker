from nonebot import on_command
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
from nonebot.adapters.cqhttp.message import MessageSegment

from utils.msg_util import MS

from .data_source import dataGet, dataProcess

__plugin_info__ = {
    "name": "网易云点歌",
    "usage": {
        "点歌 <歌名>": {"des": "搜索网易云音乐歌曲", "eg": "点歌 海阔天空"},
    },
    "author": "风屿",
    "version": "1.0.0",
    "permission": 2,
}

dataget = dataGet()

songpicker = on_command("点歌", priority=20)


@songpicker.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    args = str(event.get_message()).strip()
    if args:
        state["songName"] = args


@songpicker.got("songName", prompt="歌名是?")
async def handle_songName(bot: Bot, event: Event, state: T_State):
    songName = state["songName"]
    songIdList = await dataget.songIds(songName=songName)
    if songIdList is None:
        await songpicker.reject("没有找到这首歌，请发送其它歌名！")
    songInfoList = list()
    for songId in songIdList:
        songInfoDict = await dataget.songInfo(songId)
        songInfoList.append(songInfoDict)
    songInfoMessage = await dataProcess.mergeSongInfo(songInfoList)
    await songpicker.send(songInfoMessage)
    state["songIdList"] = songIdList


@songpicker.got("songNum")
async def handle_songNum(bot: Bot, event: Event, state: T_State):
    songIdList = state["songIdList"]
    songNum = state["songNum"]
    if not songNum.isdigit():
        await songpicker.finish()
    else:
        songNum = int(songNum)

    if songNum >= len(songIdList):
        await songpicker.reject("数字序号错误，请重选")

    selectedSongId = songIdList[int(songNum)]
    await songpicker.finish(MS.music_163(selectedSongId))
