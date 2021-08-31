import re
from nonebot.plugin import on_command, on_message
from nonebot.adapters.cqhttp import Bot, MessageEvent, GROUP, PRIVATE_FRIEND
from nonebot.typing import T_State

from .data_source import get_illust_link, get_illust_info

from service.db.utils.illust import add_illust, check_illust
from configs.config import OWNER

__permission__ = 6
__plugin_name__ = "pixiv美图上传"
__usage__ = """pixupload [pid]"""

pix_uplaod = on_command("pixupload", priority=20, permission=GROUP)

pics: dict[int, int] = {}


@pix_uplaod.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    global pics
    try:
        pid = int(event.get_plaintext().strip())
    except:
        return
    msg_id = (
        await bot.send_private_msg(
            user_id=int(OWNER),
            message=f"{event.user_id} 上传了pid为 {pid} 的图片\n链接: {await get_illust_link(pid)}",
        )
    )["message_id"]
    pics |= {msg_id: pid}


pix_check = on_message(priority=100, permission=PRIVATE_FRIEND)


@pix_check.handle()
async def _c(bot: Bot, event: MessageEvent, state: T_State):
    global pics
    if str(event.user_id) != OWNER:
        return
    if not event.reply:
        return
    reply_id = event.reply.message_id
    if reply_id not in list(pics.keys()):
        return
    nsfw = int(event.message.extract_plain_text())
    if nsfw in range(0, 3):
        if await check_illust(pics[reply_id]):
            await pix_check.finish(f"添加失败，若无报错则图片或许已在图库中")
        info = await get_illust_info(pics[reply_id])
        if info:
            info |= {"nsfw": nsfw}
            await add_illust(info)
            await bot.send(event, f"成功将 {pics[reply_id]} 的图片添加到图库中，类型: {nsfw}")
            pics.pop(reply_id)
            return
        else:
            await pix_check.finish(f"添加失败，若无报错则图片或许已被删除")
    await bot.send(event, f"拒绝将 {pics[reply_id]} 的图片添加到图库中")
    pics.pop(reply_id)
