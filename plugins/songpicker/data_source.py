import httpx

from configs.config import NETEASE_API


class dataApi:
    async def search(self, songName: str):
        async with httpx.AsyncClient() as client:
            r = await client.get(
                f"https://{NETEASE_API}/search/?keywords={songName}&limit=3&type=1&offset=0"
            )
        jsonified_r = r.json()
        if "result" not in jsonified_r:
            raise APINotWorkingException(r.text)
        return jsonified_r

    async def getSongInfo(self, songId: int):
        async with httpx.AsyncClient() as client:
            r = await client.get(
                f"https://{NETEASE_API}/song/detail/?ids={songId}",
            )
        jsonified_r = r.json()
        if "songs" not in jsonified_r:
            raise APINotWorkingException(r.text)
        return jsonified_r


class dataGet(dataApi):

    api = dataApi()

    async def songIds(self, songName: str, amount=3) -> list:
        songIds = list()
        r = await self.api.search(songName=songName)
        idRange = (
            amount if amount < len(r["result"]["songs"]) else len(r["result"]["songs"])
        )
        for i in range(idRange):
            songIds.append(r["result"]["songs"][i]["id"])
        return songIds

    async def songInfo(self, songId: int) -> dict:
        songInfo = dict()
        r = await self.api.getSongInfo(songId)
        songInfo["songName"] = r["songs"][0]["name"]
        songArtists = list()
        for ars in r["songs"][0]["ar"]:
            songArtists.append(ars["name"])
        songArtistsStr = "、".join(songArtists)
        songInfo["songArtists"] = songArtistsStr

        songInfo["songAlbum"] = r["songs"][0]["al"]["name"]

        return songInfo


class dataProcess:
    @staticmethod
    async def mergeSongInfo(songInfos: list) -> str:
        songInfoMessage = "请输入欲点播歌曲的序号：\n"
        numId = 0
        for songInfo in songInfos:
            songInfoMessage += f"{numId}："
            songInfoMessage += songInfo["songName"]
            songInfoMessage += "-"
            songInfoMessage += songInfo["songArtists"]
            songInfoMessage += " 专辑："
            songInfoMessage += songInfo["songAlbum"]
            songInfoMessage += "\n"
            numId += 1
        return songInfoMessage

    @staticmethod
    async def mergeSongComments(songComments: dict) -> str:
        songCommentsMessage = "\n".join(
            ["%s： %s" % (key, value) for (key, value) in songComments.items()]
        )
        return songCommentsMessage


class APINotWorkingException(Exception):
    def __init__(self, wrongData):
        self.uniExceptionTip = "网易云音乐接口返回了意料之外的数据：\n"
        self.wrongData = wrongData

    def __str__(self):
        return self.uniExceptionTip + self.wrongData
