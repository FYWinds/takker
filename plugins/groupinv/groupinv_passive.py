from nonebot.adapters.cqhttp import Bot, GroupRequestEvent
from nonebot.adapters.cqhttp.exception import ActionFailed
from nonebot.plugin import on_request
from nonebot.typing import T_State
from nonebot.log import logger

from api.info import get_stranger_info, get_group_member_list

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
    user_id = event.user_id
    if event.sub_type == "add":
        flag = str(event.flag)
        if str(event.group_id) in enabled_groups:
            for w in keywords:
                if w in event.comment:
                    if await check_list(str(user_id)):
                        await set_request(bot, user_id, flag, False, "请勿重复添加粉丝群")
                        return
                    if str(event.group_id) != "758550492":
                        if not await check_level(event.user_id):
                            await set_request(
                                bot, user_id, flag, False, "请不要使用等级过低的QQ小号加群,若是真人请联系管理"
                            )
                            return
                    await set_request(bot, user_id, flag, True)
                    return
            await set_request(bot, user_id, flag, False, "请认真回答并检查是否误写,提示:视频网站")


async def set_request(
    bot: Bot, user_id: int, flag: str, approve: bool, reason: str = ""
):
    try:
        await bot.set_group_add_request(
            flag=flag, sub_type="add", approve=approve, reason=reason
        )
        logger.info("通过" if approve else "拒绝" + f"了 {user_id} 的加群请求，原因 {reason}")
    except ActionFailed as e:
        f_reason = e.info["wording"]
        logger.info(f"处理 {user_id} 的加群请求失败，原因 {f_reason}")


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
