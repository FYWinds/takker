from argparse import Namespace

from db.models.statistic import Statistic
from db.utils.illust_config import IllustConfig

from .data_source import get_illust, get_illust_direct


async def handle_get(args: Namespace):
    if args.keywords:
        keywords = args.keywords
    else:
        keywords = []
    if len(keywords) == 1 and keywords[0].isdigit():
        try:
            result = await get_illust_direct(keywords[0])
            return result
        except ValueError:
            pass
    if args.group:
        await Statistic.set_illust_status(args.group, keywords)
    nsfw_level = 0
    if args.level:
        if args.level[0] in [0, 1, 2]:
            nsfw_level = args.level[0]
        else:
            nsfw_level = 0
    else:
        nsfw_level = 0
    result = await get_illust(nsfw_level, keywords)
    return result


settings: list[str] = [
    "send_tags",
    "send_image",
    "send_author",
    "send_title",
    "send_link",
]


async def handle_set(args: Namespace) -> str:
    state = bool(args.state[0])
    config = args.settings
    configs: list[str] = []
    for c in config:
        if c in settings:
            configs.append(c)
    await IllustConfig.set_illust_config(configs, state)
    return f"配置项({', '.join(configs)})修改成功!"
