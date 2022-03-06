import subprocess

from nonebot.log import logger

from db.db_connect import db_init
from utils.browser import install
from configs.config import INFO_LOG_TIME, DEBUG_LOG_TIME, ERROR_LOG_TIME
from configs.path_config import LOG_PATH
from db.utils.data_convert import convert


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
    logger.debug("Starting Migration...")
    subprocess.Popen(
        "aerich upgrade", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT
    )
    logger.debug("Migration Complete...")
    await convert()

    # *更新权限
    from db.utils.perm import Perm
    from configs.config import OWNER, SUPERUSERS

    for id in SUPERUSERS:
        await Perm.set_perm(id=id, perm=9)
    await Perm.set_perm(id=OWNER, perm=10)


def update_plugin_list(driver):
    # * 更新插件列表
    from nonebot.plugin import Plugin, get_loaded_plugins
    from nonebot.adapters import Bot

    from configs.config import HIDDEN_PLUGINS
    from db.utils.plugin_perm import PluginPerm
    from db.utils.plugin_manager import PluginManager

    @driver.on_bot_connect
    async def _update_plugin_list(bot: Bot) -> None:
        logger.info("更新插件列表中...")
        current_plugin_list: list[Plugin] = sorted(
            list(get_loaded_plugins()), key=lambda p: p.name
        )
        current_plugin_status: dict[str, bool] = {}
        group_list = await bot.get_group_list()
        user_list = await bot.get_friend_list()

        for group in group_list:
            group_id = group["group_id"]

            # 插件管理器状态更新
            plugin_status = await PluginManager.query_plugin_status(
                id=group_id, isGroup=True
            )
            for plugin_name in [plugin.name for plugin in current_plugin_list]:
                if plugin_name not in HIDDEN_PLUGINS:
                    if plugin_name not in plugin_status:
                        current_plugin_status[plugin_name] = True
                    else:
                        current_plugin_status[plugin_name] = plugin_status[plugin_name]

            await PluginManager.set_plugin_status(
                id=group_id, status=current_plugin_status, isGroup=True
            )

        for user in user_list:
            user_id = user["user_id"]
            # 插件管理器状态更新
            plugin_status = await PluginManager.query_plugin_status(id=user_id)
            for plugin_name in [plugin.name for plugin in current_plugin_list]:
                if plugin_name not in HIDDEN_PLUGINS:
                    if plugin_name not in plugin_status:
                        current_plugin_status[plugin_name] = True
                    else:
                        current_plugin_status[plugin_name] = plugin_status[plugin_name]
            await PluginManager.set_plugin_status(
                id=user_id, status=current_plugin_status
            )

        # 全局插件权限更新
        plugin_perms = await PluginPerm.get_all_plugin_perm()
        current_plugin_perms: dict[str, int] = {}
        if plugin_perms:
            for plugin in current_plugin_list:
                if plugin.name not in HIDDEN_PLUGINS:
                    plugin_info = getattr(plugin, "plugin_info", {})
                    if plugin.name not in plugin_perms:
                        current_plugin_perms[plugin.name] = plugin_info.get(
                            "permission", 5
                        )
                    else:
                        current_plugin_perms[plugin.name] = plugin_perms[plugin.name]
        else:
            for plugin in current_plugin_list:
                if plugin.name not in HIDDEN_PLUGINS:
                    plugin_info = getattr(plugin, "plugin_info", {})
                    current_plugin_perms = {
                        plugin.name: plugin_info.get("permission", 5)
                    }
        await PluginPerm.group_set_plugin_perm(current_plugin_perms)
