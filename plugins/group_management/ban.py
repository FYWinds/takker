from gocqapi import api
from nonebot.plugin import on_command
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import Bot, GroupMessageEvent

from utils.rule import admin
from utils.utils import extract_time_delta, extract_mentioned_ids
from utils.img_util import textToImage
from utils.msg_util import MS

ban = on_command(
    "禁言",
    aliases={
        "禁",
        "ban",
        "Ban",
    },
    rule=admin(),
    priority=20,
    block=True,
)


@ban.handle()
async def _ban(bot: Bot, event: GroupMessageEvent):
    at_list = await extract_mentioned_ids(event.message)
    if not at_list:
        await ban.finish("无用户被禁言")
    try:
        ban_time = await extract_time_delta(event.message)
    except ValueError:
        await ban.finish("未提取到时间段")
        return
    progress: dict[int, bool] = {}
    group_id = event.group_id
    for at_id in at_list:
        try:
            await api.set_group_ban(group_id, at_id, ban_time)
            progress[at_id] = True
        except ValueError:
            progress[at_id] = False
            fail = True
    message = f"成功{'禁言' if ban_time != 0 else '解禁'}: \n" + ", ".join(
        [str(user) for user in progress if progress[user]]
    )
    message += (
        (
            "\n 以下用户禁言失败\n"
            + ", ".join([str(user) for user in progress if not progress[user]])
        )
        if fail
        else ""
    )
    await ban.finish(MS.image(c=await textToImage(message)))
