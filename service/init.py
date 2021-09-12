# from utils.data import load_data
from utils.log import log_to_file
from utils.browser import install
from service.db.db_connect import db_init
from service.db.utils.data_convert import convert


async def init_bot():
    # 日志记录到文件中
    await log_to_file()

    # 建立数据库连接
    await db_init()

    # 检查更新Playwright的Chromuim
    await install()

    # 数据迁移
    await convert()
