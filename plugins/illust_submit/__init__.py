import re

from nonebot.plugin import on_command, on_message
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import GROUP, PRIVATE_FRIEND, Bot, MessageEvent

from configs.config import OWNER
from db.models.illust import Illust

from .data_source import get_illust_info, get_illust_link

__plugin_info__ = {
    "name": "Pixiv图片上传",
    "usage": {
        "pixupload <pid>": {"des": "上传指定PID的Pixiv图片到图库中", "eg": "pixupload 12345678"}
    },
    "additional_info": f"图片会经过 {OWNER} 审核后才上传",
    "author": "风屿",
    "version": "1.0.0",
    "permission": 6,
}

pix_uplaod = on_command("pixupload", priority=20, permission=GROUP)

pics: dict[int, int] = {}


@pix_uplaod.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    global pics
    pid = str(event.get_plaintext().strip())
    if not pid.isdigit():
        return
    pid = int(pid)
    message = f"{event.user_id} 上传了pid为 {pid} 的图片\n链接: {await get_illust_link(pid)}"
    data = await bot.send_private_msg(user_id=int(OWNER), message=message)
    msg_id = data["message_id"]
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
        if await Illust.check_illust(pics[reply_id]):
            await pix_check.finish("添加失败，若无报错则图片或许已在图库中")
        info = await get_illust_info(pics[reply_id])
        if info:
            info |= {"nsfw": nsfw}
            await Illust.add_illust(info)
            await bot.send(event, f"成功将 {pics.pop(reply_id)} 的图片添加到图库中，类型: {nsfw}")
            return
        else:
            await pix_check.finish("添加失败，若无报错则图片或许已被删除")
    await bot.send(event, f"拒绝将 {pics.pop(reply_id)} 的图片添加到图库中")
