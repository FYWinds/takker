"""
Author: FYWindIsland
Date: 2021-08-10 10:04:37
LastEditTime: 2021-08-13 08:48:02
LastEditors: FYWindIsland
Description: 
I'm writing SHIT codes
"""
from utils.patcher import patch

# from utils.data import load_data
from service.log import log_to_file
from service.db.database_sqlite import db_init


async def init_bot():
    # 日志记录到文件中
    await log_to_file()

    # 建立数据库连接
    await db_init()

    # 为windows下的playwright的异步注入猴子补丁
    # patch()  # 改框架源码了，不注入了

    # # 载入只读不写的数据到内存中
    # load_data()
