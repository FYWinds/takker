import json
import shutil

from nonebot.log import logger
from tortoise.query_utils import Q

from configs.path_config import DATA_PATH
from db.models.config import VERSION_TAG, BotConfig, UserConfig, GroupConfig
from db.models.outdated_models import Point, Plugin, Starluck, Permission


async def convert() -> None:
    if await BotConfig.get_or_none(id=1):
        data_version = (
            await BotConfig.get_or_none(id=1)
            if await BotConfig.get_or_none(id=1)
            else ""
        ).version  # type: ignore
        if data_version != VERSION_TAG:
            logger.info(f"检测到旧版({data_version})数据，正在转换中")
            logger.info("如数据出现问题请回滚版本并用data/data.db.old覆盖data/data.db，并向开发者提Issue")
            shutil.copyfile(f"{DATA_PATH}data.db", f"{DATA_PATH}data.db.old")

            if data_version == "1.0.0":
                await convert_perm()
                await convert_star()
                await convert_points()
                await convert_pstatus()
                await BotConfig.filter(Q(id=1)).update(version="1.1.0")

            logger.success("数据转换完成，请人工确认数据是否有丢失情况")
            return
        return
    else:
        await BotConfig.create(version=VERSION_TAG)
        await convert()


async def convert_star() -> None:
    current_data = await Starluck.filter().values()
    for star in current_data:
        await UserConfig.update_or_create(
            uid=int(star["uid"]), defaults={"constellation": int(star["star"])}
        )


async def convert_perm() -> None:
    current_data = await Permission.filter().values()
    for data in current_data:
        perm = int(data["perm"])
        if str(data["id"]).isdigit():
            uid = int(data["id"])
            await UserConfig.update_or_create(uid=uid, defaults={"perm": perm})
        else:
            gid = int(data["id"][1:])
            await GroupConfig.update_or_create(gid=gid, defaults={"perm": perm})


async def convert_points() -> None:
    current_data = await Point.filter().values()
    for data in current_data:
        await UserConfig.update_or_create(
            uid=int(data["uid"]), defaults={"points": int(data["points"])}
        )


async def convert_pstatus() -> None:
    current_data = await Plugin.filter().values()
    for data in current_data:
        if str(data["id"]).isdigit():
            uid = int(data["id"])
            await UserConfig.update_or_create(
                uid=uid,
                defaults={
                    "plugin_status": json.loads(
                        str(data["status"])
                        .replace("'", '"')
                        .replace("True", "true")
                        .replace("False", "false")
                        .replace("None", "null")
                    )
                },
            )
        else:
            gid = int(data["id"][1:])
            await GroupConfig.update_or_create(
                gid=gid,
                defaults={
                    "plugin_status": json.loads(
                        str(data["status"])
                        .replace("'", '"')
                        .replace("True", "true")
                        .replace("False", "false")
                        .replace("None", "null")
                    )
                },
            )
