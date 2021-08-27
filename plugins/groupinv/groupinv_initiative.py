from nonebot_plugin_apscheduler import scheduler
from nonebot.log import logger
from nonebot.adapters.cqhttp.exception import ActionFailed

from api.group_manage import set_request
from api.info import get_stranger_info, group_join_request, get_group_member_list


__permission__ = 0

__plugin_name__ = "加群自动审核"

__usage__ = """无指令
"""


@scheduler.scheduled_job("interval", seconds=10, id="handle_group_req")
async def handle_group_requests():
    approve = False
    agree_keyword = [
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
    if not req:
        return
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
    flag = str(reqs["request_id"])
    requester_nick = reqs["requester_nick"]
    requester_uin = reqs["requester_uin"]
    group_id = reqs["group_id"]
    group_name = reqs["group_name"]
    try:
        await set_request(flag, True)
    except ActionFailed as e:
        f_reason = e.info["wording"]
        logger.info(
            f"处理 {requester_nick}({requester_uin}) 加入 {group_name}({group_id}) 的加群请求，失败原因: {f_reason}"
        )
    logger.info(
        f"通过了 {requester_nick}({requester_uin}) 加入 {group_name}({group_id}) 的加群请求"
    )


async def reject_requests(reqs: dict, reason: str):
    flag = str(reqs["request_id"])
    requester_nick = reqs["requester_nick"]
    requester_uin = reqs["requester_uin"]
    group_id = reqs["group_id"]
    group_name = reqs["group_name"]
    try:
        await set_request(flag, False, reason)
    except ActionFailed as e:
        f_reason = e.info["wording"]
        logger.info(
            f"处理 {requester_nick}({requester_uin}) 加入 {group_name}({group_id}) 的加群请求，失败原因: {f_reason}"
        )
    logger.info(
        f"拒绝了 {requester_nick}({requester_uin}) 加入 {group_name}({group_id}) 的加群请求\n原因：{reason}"
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


async def check_level(reqs: dict):
    r = await get_stranger_info(reqs["requester_uin"])
    if r["level"] >= 5:
        return True
    else:
        return False
