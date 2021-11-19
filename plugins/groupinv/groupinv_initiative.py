from nonebot.log import logger
from nonebot_plugin_apscheduler import scheduler
from nonebot.adapters.cqhttp.exception import ActionFailed

from api import API
from api.models import JoinRequest

api = API()


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

    reqs = (await api.get_group_system_msg()).join_requests
    if not reqs:
        return
    for req in reqs:
        if req.suspicious:
            continue
        if not req.checked:
            if req.group_id in grouplist:
                if await check_list(req.requester_uin):
                    await reject_requests(req, "请勿重复添加粉丝群")
                    continue
                if not await check_level(req):
                    await reject_requests(req, "请不要使用等级过低的QQ小号加群,若是真人请联系管理")
                    break
                for keyword in agree_keyword:
                    if keyword in req.message:
                        approve = True
                        break
                if not approve:
                    await reject_requests(req, "请认真回答并检查是否误写,提示:视频网站")
                    break
        if approve:
            await approve_requests(req)


async def approve_requests(req: JoinRequest):
    flag = str(req.request_id)
    requester_nick = req.requester_nick
    requester_uin = req.requester_uin
    group_id = req.group_id
    group_name = req.group_name
    try:
        await api.set_group_add_request(flag, "add", approve=True)
        logger.info(
            f"通过了 {requester_nick}({requester_uin}) 加入 {group_name}({group_id}) 的加群请求"
        )
    except ActionFailed as e:
        f_reason = e.info["wording"]
        logger.info(
            f"处理 {requester_nick}({requester_uin}) 加入 {group_name}({group_id}) 的加群请求，失败原因: {f_reason}"
        )


async def reject_requests(req: JoinRequest, reason: str):
    flag = str(req.request_id)
    requester_nick = req.requester_nick
    requester_uin = req.requester_uin
    group_id = req.group_id
    group_name = req.group_name
    try:
        await api.set_group_add_request(flag, "add", approve=False, reason=reason)
        logger.info(
            f"拒绝了 {requester_nick}({requester_uin}) 加入 {group_name}({group_id}) 的加群请求\n原因：{reason}"
        )
    except ActionFailed as e:
        f_reason = e.info["wording"]
        logger.info(
            f"处理 {requester_nick}({requester_uin}) 加入 {group_name}({group_id}) 的加群请求，失败原因: {f_reason}"
        )


async def check_list(user_id: int):
    # g1 = await get_group_member_list(511467246)
    g2 = await api.get_group_member_list(319152433)
    g3 = await api.get_group_member_list(603809278)
    g4 = await api.get_group_member_list(869202661)

    # for data in g1:
    #     if user_id == str(data['user_id']):
    #         return True
    for data in g2:
        if user_id == data.user_id:
            return True
    for data in g3:
        if user_id == data.user_id:
            return True
    for data in g4:
        if user_id == data.user_id:
            return True


async def check_level(req: JoinRequest):
    r = await api.get_stranger_info(req.requester_uin)
    if r.level >= 15:
        return True
    else:
        return False
