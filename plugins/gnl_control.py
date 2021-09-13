from rcon import rcon
from nonebot.plugin import on_command
from nonebot.adapters.cqhttp import Bot, MessageEvent

from configs.config import SPECIAL_IP, SUPERUSERS, SPECIAL_PASS

__permission__ = 9
__plugin_name__ = "远程执行mc指令-jpgnl专用"
__usage__ = "sudo <指令>"

command = on_command("sudo", priority=20)


@command.handle()
async def _(bot: Bot, event: MessageEvent):
    if (
        not event.sender.role in ["admin", "owner"]
        and str(event.sender.user_id) not in SUPERUSERS
    ):
        return
    c = event.get_plaintext().strip()
    result = await rcon(c, host=SPECIAL_IP, port=25575, passwd=SPECIAL_PASS)
    await command.finish(result)