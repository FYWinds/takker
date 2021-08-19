"""
Author: FYWindIsland
Date: 2021-08-19 21:55:45
LastEditTime: 2021-08-19 22:07:08
LastEditors: FYWindIsland
Description: 
I'm writing SHIT codes
"""
from nonebot.adapters.cqhttp import Bot, GroupRequestEvent
from nonebot.plugin import on_request
from nonebot.typing import T_State
from nonebot.log import logger

from api.info import get_stranger_info, get_group_member_list
from api.group_manage import set_request

gr = on_request(priority=1)

enabled_groups = [
    "511467246",
    "319152433",
    "603809278",
    "869202661",
    "758550492",
    "521656488",
]

keywords = [
    "b站",
    "B站",
    "bi",
    "Bi",
    "li",
    "破站",
    "直播",
    "投稿",
    "联合",
    "红叔",
    "优酷",
    "哔哩",
    "BILI",
    "合作",
]


@gr.handle()
async def _(bot: Bot, event: GroupRequestEvent, state: T_State):
    if event.sub_type == "add":
        if str(event.group_id) in enabled_groups:
            for w in keywords:
                if w in event.comment:
                    if not await check_list(str(event.user_id)):
                        await bot.set_group_add_request(
                            flag=event.flag,
                            sub_type="add",
                            approve=False,
                            reason="请勿重复加群",
                        )
                    if str(event.group_id) != "758550492":
                        if not await check_level(event.user_id):
                            await bot.set_group_add_request(
                                flag=event.flag,
                                sub_type="add",
                                approve=False,
                                reason="请不要使用等级过低的QQ小号加群,若是真人请联系管理",
                            )
                    await bot.set_group_add_request(
                        flag=event.flag, sub_type="add", approve=True
                    )
                else:
                    await bot.set_group_add_request(
                        flag=event.flag,
                        sub_type="add",
                        approve=False,
                        reason="请认真回答并检查是否误写,提示:视频网站",
                    )


async def check_list(user_id: str):
    # g1 = await get_group_member_list(511467246)
    g2 = await get_group_member_list(319152433)
    g3 = await get_group_member_list(603809278)
    g4 = await get_group_member_list(869202661)

    # for data in g1:
    #     if user_id == str(data['user_id']):
    #         return True
    for data in g2:
        if user_id == str(data["user_id"]):
            return True
    for data in g3:
        if user_id == str(data["user_id"]):
            return True
    for data in g4:
        if user_id == str(data["user_id"]):
            return True


async def check_level(user_id: int):
    r = await get_stranger_info(user_id)
    if r["level"] >= 5:
        return True
    else:
        return False
