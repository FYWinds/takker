import httpx
from nonebot.plugin import on_command
from nonebot.adapters.cqhttp import Bot, MessageEvent

from utils.rule import limit_group
from configs.config import SPECIAL_URL, SPECIAL_TOKEN
from utils.img_util import textToImage
from utils.msg_util import image

__permission__ = 9
__plugin_name__ = "建平查分工具"
__usage__ = "查分 <年级>"

command = on_command("查分", priority=20, rule=limit_group(["521656488", "765321243"]))


@command.handle()
async def _(bot: Bot, event: MessageEvent):
    grade = event.get_plaintext().strip()
    print(grade)
    if not grade.isdigit():
        return
    grade = int(grade)
    if grade not in [17, 18, 19, 20, 21]:
        return
    async with httpx.AsyncClient() as client:
        r = await client.get(
            f"https://{SPECIAL_URL}?token={SPECIAL_TOKEN}&grade={grade}"
        )
    data: dict[str, dict[str, dict[str, dict[str, float]]]] = r.json()
    if "retcode" not in data or data["retcode"] != 0:
        return
    message: list[str] = ["成绩获取为随机抽取对应年级学号获取，无法保证涵盖各分层班"]
    for i in range(2):
        exam = list(data["data"].keys())[i]
        message.append(exam)
        for course in data["data"][exam]:
            message.append(f"    {course}:")
            for k, v in data["data"][exam][course].items():
                message.append(f"        {k}: {v}")
    msg = "\n".join(message)
    img = await textToImage(msg, cut=100)
    await command.finish(image(c=img))
