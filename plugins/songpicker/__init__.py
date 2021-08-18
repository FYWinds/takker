"""
Author: FYWindIsland
Date: 2021-08-18 10:34:02
LastEditTime: 2021-08-18 11:21:48
LastEditors: FYWindIsland
Description: 
I'm writing SHIT codes
"""
from nonebot.adapters import Bot, Event
from nonebot.typing import T_State
from nonebot import on_command
from nonebot.adapters.cqhttp.message import MessageSegment

from utils.msg_util import music_163

from .data_source import dataGet, dataProcess

__permission__ = 2
__plugin_name__ = "点歌"
__usage__ = "点歌 歌名"


dataget = dataGet()

songpicker = on_command("点歌")


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
    await songpicker.finish(music_163(selectedSongId))
