import os

from nonebot.log import logger

from configs.path_config import DATA_PATH


async def shut_down():
    logger.info("关闭中，正在清理缓存与保存数据")

    # 清理数据库回滚产生的备份缓存
    db_rollback = list(
        filter(lambda x: x.endswith(".db_rollback"), os.listdir(f"{DATA_PATH}backups/"))
    )
    for rollback in db_rollback:
        os.remove(f"{DATA_PATH}backups/{rollback}")
