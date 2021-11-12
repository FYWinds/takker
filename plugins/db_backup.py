import os
import time
import shutil

from nonebot.log import logger
from nonebot.plugin import on_command
from nonebot.typing import T_State
from tortoise.transactions import in_transaction
from nonebot.adapters.cqhttp import PRIVATE, Bot, PrivateMessageEvent
from nonebot_plugin_apscheduler import scheduler

from utils.rule import admin
from db.db_connect import db_disconnect, connect_database
from configs.config import DB_BACKUP_COPIES, DB_BAKCUP_INTERVAL
from configs.path_config import DATA_PATH

__plugin_info__ = {
    "name": "数据库备份",
    "version": "1.5.0",
    "author": "风屿",
    "des": "自动定时备份数据库，并提供回滚功能",
    "superuser_usage": {
        "backup list": "查看备份列表",
        "backup rollback": "回滚到指定备份",
    },
    "permission": 9,
}


# 定时任务
@scheduler.scheduled_job("interval", minutes=DB_BAKCUP_INTERVAL)
async def backup_db():
    logger.info("开始备份数据库")
    async with in_transaction("data") as conn:
        await conn.execute_query("PRAGMA wal_checkpoint(FULL)")

    current_backups = list(
        filter(lambda x: x.endswith(".db"), os.listdir(f"{DATA_PATH}backups"))
    )
    if len(current_backups) >= DB_BACKUP_COPIES:
        current_backups.sort()
        os.remove(f"{DATA_PATH}backups/{current_backups[0]}")
    shutil.copyfile(
        f"{DATA_PATH}data.db", f"{DATA_PATH}backups/data_{int(time.time())}.db"
    )
    logger.debug("数据库备份完成")


# 查看/回滚备份
db_backup = on_command(
    "backup", priority=20, rule=admin(True), permission=PRIVATE, block=True
)


@db_backup.handle()
async def _(bot: Bot, event: PrivateMessageEvent, state: T_State):
    backups = list(
        filter(lambda x: x.endswith(".db"), os.listdir(f"{DATA_PATH}backups"))
    )
    backups.sort()
    state["backupList"] = backups
    backups = [
        "创建时间"
        + time.strftime(
            "%Y-%m-%d %H:%M:%S", time.localtime(int(b.split("_")[1].split(".")[0]))
        )
        for b in backups
    ]
    bk: list[str] = []
    for index, backup in enumerate(backups):
        bk.append(f"{index + 1}. {backup}")
    line = "\n"
    result = f"自动备份列表：\n{line.join(bk)}"
    msg = str(event.message).strip()
    if msg == "list":
        await db_backup.finish(result)
    if msg == "rollback":
        await bot.send(event, result)
        await bot.send(event, "发送要回滚的数字序号")


@db_backup.got("backupNum")
async def _a(bot: Bot, event: PrivateMessageEvent, state: T_State):
    backupNum = state["backupNum"]
    if not backupNum.isdigit():
        await db_backup.finish()
    backupNum = int(backupNum)
    if backupNum > len(state["backupList"]):
        await db_backup.reject("超出范围")
    backupList: list[str] = state["backupList"]
    backup = backupList[backupNum - 1]
    state["backup"] = backup
    await bot.send(event, f"确认要回滚到{backup}吗？[y/N]\n回滚过程可能造成机器人无法处理信息，且将丢失备份以来所有新增数据")


@db_backup.got("confirm")
async def _b(bot: Bot, event: PrivateMessageEvent, state: T_State):
    if state["confirm"] == "y" or state["confirm"] == "Y":
        try:
            backup = state["backup"]
            await bot.send(event, f"正在回滚到{backup} 中")
            await db_disconnect()
            state[
                "rollbackBackupFileName"
            ] = f"data_rollback_backup-{int(time.time())}.db_rollback"
            shutil.copyfile(
                f"{DATA_PATH}data.db",
                f"{DATA_PATH}backups/{state['rollbackBackupFileName']}",
            )
            os.remove(f"{DATA_PATH}data.db")
            await bot.send(
                event, f"将当前数据库备份在 {DATA_PATH}backups/{state['rollbackBackupFileName']}"
            )
            shutil.copyfile(f"{DATA_PATH}backups/{backup}", f"{DATA_PATH}data.db")
            await connect_database()
            await bot.send(event, f"成功回滚到 {backup} 的数据，若希望撤销回滚请发送 取消回滚")
        except Exception:
            await bot.send(event, "回滚失败，请尝试手动恢复数据")
    else:
        await db_backup.finish()


@db_backup.got("cancel")
async def _c(bot: Bot, event: PrivateMessageEvent, state: T_State):
    if (
        state["cancel"] == "撤销回滚"
        or state["cancel"] == "取消回滚"
        or state["cancel"] == "取消"
        or state["cancel"] == "撤销"
        or state["cancel"] == "cancel"
        or state["cancel"] == "Cancel"
    ):
        try:
            rollbackBackupFileName = state["rollbackBackupFileName"]
            await bot.send(event, "正在撤销回滚中")
            await db_disconnect()
            shutil.copyfile(
                f"{DATA_PATH}backups/{rollbackBackupFileName}",
                f"{DATA_PATH}data.db",
            )
            os.remove(f"{DATA_PATH}backups/{rollbackBackupFileName}")
            await connect_database()
            await bot.send(event, "成功撤销回滚的数据")
        except Exception:
            await bot.send(event, "撤销失败，请尝试手动恢复数据")
    else:
        await db_backup.finish()
