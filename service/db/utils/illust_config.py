from typing import Union, Optional

from service.db.models.config import BotConfig

default_config: dict[str, bool] = {
    "send_tags": True,  # 是否发送tags
    "send_image": True,  # 是否发送图片
    "send_author": True,  # 是否发送作者和uid
    "send_title": True,  # 是否发送图片名字
    "send_link": True,  # 是否发送原图链接
}


async def get_illust_config() -> dict[str, bool]:
    config = await BotConfig.get_or_none(id=1)
    if config and config.illust_config:
        return config.illust_config
    else:
        await _init_illust_config()
        return await get_illust_config()


async def _init_illust_config() -> None:
    await BotConfig.update_or_create(id=1, defaults={"illust_config": default_config})


async def set_illust_config(config: Union[str, list[str]], status: bool) -> None:
    current_config = await get_illust_config()
    if isinstance(config, str):
        current_config[config] = status
    elif isinstance(config, list):
        for c in config:
            current_config[c] = status
    await BotConfig.update_or_create(id=1, defaults={"illust_config": current_config})
