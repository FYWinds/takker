from typing import Union

import httpx
from tortoise.models import Model
from tortoise.fields.data import IntField, CharField, BooleanField
from tortoise.query_utils import Q


class Bili_sub(Model):
    type = CharField(max_length=10)  # 订阅类型 user/group
    type_id = IntField()  # 订阅会话id
    bid = IntField()  # 订阅主播
    name = CharField(max_length=30)  # 主播名字
    live = BooleanField(default=True)  # 是否订阅直播 默认为True
    dynamic = BooleanField(default=True)  # 是否订阅动态 默认为True
    at = BooleanField(default=False)  # 是否在是群管理员的情况下at全体 默认为False

    class Meta:
        table = "bili_sub"
        table_description = "b站订阅数据"
        indexes = ("type_id", "bid")

    @classmethod
    async def get_sub(
        cls, id: Union[str, int], isGroup: bool = False
    ) -> dict[int, str]:
        """
        :说明: `get_sub`
        > 获取指定会话的订阅列表

        :参数:
          * `id: Union[str, int]`: 会话id qq或群号

        :可选参数:
          * `isGroup: bool = False`: 是否是群组

        :返回:
          - `dict[int, str]`: 订阅列表 {主播BID: "主播名字"}
        """
        if isGroup:
            data = await cls.filter(type="group", type_id=int(id)).values()
        else:
            data = await cls.filter(type="user", type_id=int(id)).values()
        sub_list: dict[int, str] = {}
        if data:
            for sub in data:
                sub_list |= {sub["bid"]: sub["name"]}
        return sub_list

    @classmethod
    async def get_all_sub(cls) -> dict[str, dict[int, dict[int, str]]]:
        """
        :说明: `get_all_sub`
        > 获取所有的订阅列表

        :返回:
          - `dict[str, dict[int, dict[int, str]]]`: 订阅列表
          {"group": {群号: {主播BID: "主播名字"}}, "user": {}}
        """
        data = await cls.filter().values()
        sub_list: dict[str, dict[int, dict[int, str]]] = {"group": {}, "user": {}}
        # {"group": {1234556: {5007752: "萝卜吃米洛", "19238938": "风屿"}}, "user": {}}
        if data:
            for sub in data:
                bid = sub["bid"]
                name = sub["name"]
                type = sub["type"]
                type_id = sub["type_id"]
                if type == "user":
                    try:
                        prev_sub_list = sub_list["user"][type_id]
                    except:
                        prev_sub_list = {}
                    prev_sub_list |= {bid: name}
                    sub_list["user"] |= {type_id: prev_sub_list}
                if type == "group":
                    try:
                        prev_sub_list = sub_list["group"][type_id]
                    except:
                        prev_sub_list = {}
                    prev_sub_list |= {bid: name}
                    sub_list["group"] |= {type_id: prev_sub_list}
        return sub_list

    @classmethod
    async def add_record(
        cls, id: Union[str, int], bid: Union[str, int], isGroup: bool = False
    ) -> bool:
        try:
            name = await cls.get_user_name(bid)
        except:
            return False
        if isGroup:
            if await cls.get_or_none(type="group", type_id=int(id), bid=int(bid)):
                return False
            await cls.create(
                type="group",
                type_id=int(id),
                bid=int(bid),
                name=str(name),
                live=True,
                dynamic=True,
                at=False,
            )
        else:
            if await cls.get_or_none(type="user", type_id=int(id), bid=int(bid)):
                return False
            await cls.create(
                type="user",
                type_id=int(id),
                bid=int(bid),
                name=str(name),
                live=True,
                dynamic=True,
                at=False,
            )
        return True

    @classmethod
    async def remove_record(
        cls, id: Union[str, int], bid: Union[str, int], isGroup: bool = False
    ) -> bool:
        try:
            if isGroup:
                if not await cls.get_or_none(
                    type="group", type_id=int(id), bid=int(bid)
                ):
                    return False
                await cls.filter(type="group", type_id=int(id), bid=int(bid)).delete()
            else:
                if not await cls.get_or_none(
                    type="user", type_id=int(id), bid=int(bid)
                ):
                    return False
                await cls.filter(type="user", type_id=int(id), bid=int(bid)).delete()
        except:
            return False
        return True

    @classmethod
    async def get_settings(
        cls,
        id: Union[str, int],
        bid: Union[str, int],
        isGroup: bool = False,
    ) -> dict[str, bool]:
        if isGroup:
            data = await cls.get_or_none(type="group", type_id=int(id), bid=int(bid))
        else:
            data = await cls.get_or_none(type="user", type_id=int(id), bid=int(bid))
        if data:
            assert data.at is not None
            assert data.live is not None
            assert data.dynamic is not None
            return {
                "at": bool(data.at),
                "live": bool(data.live),
                "dynamic": bool(data.dynamic),
            }
        return {}

    @classmethod
    async def edit_settings(
        cls, id: Union[str, int], bid: Union[str, int], set: str, isGroup: bool = False
    ) -> None:
        current_settings = await cls.get_settings(id, bid, isGroup)
        if not current_settings:
            return
        current_settings[set] = not current_settings[set]
        if isGroup:
            await cls.filter(type="group", type_id=int(id), bid=int(bid)).update(
                at=current_settings["at"],
                live=current_settings["live"],
                dynamic=current_settings["dynamic"],
            )
        else:
            await cls.filter(type="user", type_id=int(id), bid=int(bid)).update(
                at=current_settings["at"],
                live=current_settings["live"],
                dynamic=current_settings["dynamic"],
            )

    @classmethod
    async def get_user_name(cls, bid: Union[str, int]) -> str:
        data = await cls.filter(bid=int(bid)).values()
        if data:
            return data[0]["name"]
        else:
            return (await get_user_info(bid))["data"]["card"]["name"]

    @classmethod
    async def get_live_bid(cls) -> list[int]:
        data = await cls.filter(live=True).values()
        uids: list[int] = []
        for u in data:
            uids.append(u["bid"])
        return list(set(uids))

    @classmethod
    async def get_live_push_list(cls, bid: Union[str, int]) -> dict[str, list[int]]:
        data = await cls.filter(bid=int(bid), live=True).values()
        live_push_list: dict[str, list[int]] = {"group": [], "user": []}
        for i in data:
            if i["type"] == "group":
                live_push_list["group"].append(i["type_id"])
            elif i["type"] == "user":
                live_push_list["user"].append(i["type_id"])
        return live_push_list

    @classmethod
    async def get_dynamic_bid(cls) -> list[int]:
        data = await cls.filter(dynamic=True).values()
        uids: list[int] = []
        for u in data:
            uids.append(u["bid"])
        return list(set(uids))

    @classmethod
    async def get_dynamic_push_list(cls, bid: Union[str, int]) -> dict[str, list[int]]:
        data = await cls.filter(bid=int(bid), dynamic=True).values()
        dynamic_push_list: dict[str, list[int]] = {"group": [], "user": []}
        for i in data:
            if i["type"] == "group":
                dynamic_push_list["group"].append(i["type_id"])
            elif i["type"] == "user":
                dynamic_push_list["user"].append(i["type_id"])
        return dynamic_push_list


API_URL = "https://hibi.windis.xyz/api/bilibili/v3/"


async def get_user_info(bid: Union[int, str]) -> dict:
    url = f"{API_URL}user_info"
    params = {"uid": bid, "size": 1}
    async with httpx.AsyncClient() as client:
        resp = await client.get(url, params=params)
    return resp.json()
