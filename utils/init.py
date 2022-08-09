from logging import INFO

from nonebot.log import logger

from utils.browser import install
from configs.config import INFO_LOG_TIME, DEBUG_LOG_TIME, ERROR_LOG_TIME
from configs.path_config import LOG_PATH
from service.db.db_connect import db_init
from service.db.utils.data_convert import convert


async def init_bot_startup():
    # *日志记录到文件中

    custom_format = (
        "<g>{time:YYYY-MM-DD HH:mm:ss}</g> " "[{level}] " "{name} | " "{message}"
    )
    logger.add(
        LOG_PATH + "debug/{time:YYYY-MM-DD}.log",
        rotation="00:00",
        retention=f"{DEBUG_LOG_TIME} days",
        level="DEBUG",
        format=custom_format,
        encoding="utf-8",
    )
    logger.add(
        LOG_PATH + "info/{time:YYYY-MM-DD}.log",
        rotation="00:00",
        retention=f"{INFO_LOG_TIME} days",
        level="INFO",
        format=custom_format,
        encoding="utf-8",
    )
    logger.add(
        LOG_PATH + "error/{time:YYYY-MM-DD}.log",
        rotation="00:00",
        retention=f"{ERROR_LOG_TIME} days",
        level="ERROR",
        format=custom_format,
        encoding="utf-8",
    )

    # *建立数据库连接
    await db_init()

    # *检查更新Playwright的Chromuim
    await install()

    # *数据迁移
    await convert()

    # *更新权限
    from configs.config import OWNER, SUPERUSERS
    from service.db.utils.perm import set_perm

    for id in SUPERUSERS:
        await set_perm(id=id, perm=9)
    await set_perm(id=OWNER, perm=10)


def update_plugin_list(driver):
    # * 更新插件列表
    from nonebot import get_driver
    from nonebot.plugin import get_loaded_plugins
    from nonebot.adapters import Bot

    from api.info import get_group_list, get_friend_list
    from configs.config import HIDDEN_PLUGINS
    from service.db.utils.plugin_manager import set_plugin_status, query_plugin_status

    @driver.on_bot_connect
    async def _update_plugin_list(bot: Bot) -> None:
        logger.info("更新插件列表")
        plugin_list_current: dict[str, bool] = {}
        group_list = await get_group_list()
        user_list = await get_friend_list()
        plugin_list = get_loaded_plugins()
        for group in group_list:
            group_id = group["group_id"]
            plugin_list_stored = await query_plugin_status(id=group_id, isGroup=True)
            # 获取当前存储的插件列表
            for p in plugin_list:
                if str(p.name) not in HIDDEN_PLUGINS:
                    plugin_list_current |= {str(p.name): True}
            # 更新插件列表至当前加载的插件列表
            if plugin_list_stored:
                for i in list(plugin_list_stored.keys()):
                    if i not in plugin_list_current.keys():
                        plugin_list_stored.pop(i)
                plugin_list_current |= plugin_list_stored
            await set_plugin_status(
                id=group_id, status=plugin_list_current, isGroup=True
            )
        for user in user_list:
            user_id = user["user_id"]
            plugin_list_stored = await query_plugin_status(id=user_id, isGroup=False)
            # 获取当前存储的插件列表
            for p in plugin_list:
                if str(p.name) not in HIDDEN_PLUGINS:
                    plugin_list_current |= {str(p.name): True}
            # 更新插件列表至当前加载的插件列表
            if plugin_list_stored:
                for i in list(plugin_list_stored.keys()):
                    if i not in plugin_list_current.keys():
                        plugin_list_stored.pop(i)
                plugin_list_current |= plugin_list_stored
            await set_plugin_status(
                id=user_id, status=plugin_list_current, isGroup=False
            )
