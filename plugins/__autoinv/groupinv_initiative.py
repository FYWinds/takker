from nonebot import drivers
from nonebot_plugin_apscheduler import scheduler
from nonebot.log import logger

from api.group_manage import set_request
from api.info import stranger_info, group_join_request, group_member_list


@scheduler.scheduled_job("interval", seconds=3, id="handle_group_req")
async def handle_group_requests():
    approve = False
    agree_keyword = [
        "b站",
        "B站",
        "bi",
        "Bi",
        "li",
        "破站",
        "视频",
        "直播",
        "投稿",
        "联合",
        "红叔",
        "优酷",
        "哔哩",
        "BILI",
        "合作",
    ]
    grouplist = [
        "511467246",
        "319152433",
        "603809278",
        "869202661",
        "758550492",
        "521656488",
    ]
    # * 一群 二群 三群 四群 直播通知群 测试群

    req = await group_join_request()

    for reqs in req:
        if str(reqs["suspicious"]) == "True":
            continue
        if str(reqs["checked"]) == "False":
            if str(reqs["group_id"]) in grouplist:
                if await check_list(str(reqs["requester_uin"])):
                    await reject_requests(reqs, "请勿重复添加粉丝群")
                    continue
                if not await check_level(reqs):
                    await reject_requests(reqs, "请不要使用等级过低的QQ小号加群,若是真人请联系管理")
                    break
                for keyword in agree_keyword:
                    if keyword in reqs["message"]:
                        approve = True
                        break
                if not approve:
                    await reject_requests(reqs, "请认真回答并检查是否误写,提示:视频网站")
                    break
        if approve:
            await approve_requests(reqs)


async def approve_requests(reqs: dict):
    flag = reqs["request_id"]
    await set_request(flag, True)
    requester_nick = reqs["requester_nick"]
    requester_uin = reqs["requester_uin"]
    group_id = reqs["group_id"]
    group_name = reqs["group_name"]
    logger.info(
        f"通过了 {requester_nick}({requester_uin}) 加入 {group_name}({group_id}) 的加群请求"
    )


async def reject_requests(reqs: dict, reason: str):
    flag = reqs["request_id"]
    await set_request(flag, False, reason)
    requester_nick = reqs["requester_nick"]
    requester_uin = reqs["requester_uin"]
    group_id = reqs["group_id"]
    group_name = reqs["group_name"]
    logger.info(
        f"拒绝了 {requester_nick}({requester_uin}) 加入 {group_name}({group_id}) 的加群请求\n原因：{reason}"
    )


async def check_list(user_id: str):
    # g1 = await group_member_list(511467246)
    g2 = await group_member_list(319152433)
    g3 = await group_member_list(603809278)
    g4 = await group_member_list(869202661)

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


async def check_level(reqs: dict):
    r = await stranger_info(reqs["requester_uin"])
    if r["level"] >= 5:
        return True
    else:
        return False
