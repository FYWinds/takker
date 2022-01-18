from gocqapi import api
from nonebot.plugin import on_command
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import Bot, GroupMessageEvent

from utils.rule import admin
from utils.utils import extract_mentioned_ids
from utils.img_util import textToImage
from utils.msg_util import MS

kick = on_command("kick", aliases={"踢人", "踢出"}, rule=admin(), priority=20, block=True)


@kick.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    at_list = await extract_mentioned_ids(event.message)
    if not at_list:
        await kick.finish("无用户被踢出群聊")
    progress: dict[int, bool] = {}
    group_id = event.group_id
    for at_id in at_list:
        try:
            await api.set_group_kick(group_id, at_id)
            progress[at_id] = True
        except ValueError:
            fail = False
            progress[at_id] = False
    message = "成功踢出: \n" + ", ".join([str(user) for user in progress if progress[user]])
    message += (
        (
            "\n 以下用户踢出失败\n"
            + ", ".join([str(user) for user in progress if not progress[user]])
        )
        if fail
        else ""
    )
    await kick.finish(MS.image(c=await textToImage(message)))
