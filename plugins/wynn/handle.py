import datetime
import zoneinfo
from typing import Any
from argparse import Namespace

from dateutil import parser as dateparser
from pydantic import ValidationError
from nonebot.log import logger

from utils.text_util import align

from .model import Stat
from .template import (
    item_stat,
    player_stat,
    server_stat,
    item_stat_verbose,
    player_stat_verbose,
    server_stat_verbose,
)
from .data_source import (
    search_item,
    get_player_info,
    get_player_uuid,
    get_player_info_v3,
)
from .data_storage import get_data, set_data

utc_tz = zoneinfo.ZoneInfo("UTC")
sh_tz = zoneinfo.ZoneInfo("Asia/Shanghai")


async def handle_bind(args: Namespace) -> str:
    data = get_data()
    try:
        name = args.name
        uid = args.uid
        uuid = (await get_player_uuid(name))["data"][0]["uuid"]
        data["bindings"][uid] = {"name": name, "uuid": uuid}
    except (KeyError, IndexError):
        return "参数错误: 玩家不存在"
    set_data(data)
    return f"绑定成功!\nid: {uid}\n游戏名: {name}\nUUID: {uuid}"


async def handle_stat(args: Namespace) -> str:
    data = get_data()
    name = args.name
    uid = args.uid
    if name is None:
        try:
            uuid = data["bindings"][uid]["uuid"]
            stats = Stat(**(await get_player_info(uuid)))
            info_v3 = await get_player_info_v3(uuid)
        except KeyError:
            return "参数错误: 未绑定ID"
        except ValidationError:
            return "数据错误: API可能暂时无法访问或已更新"
    else:
        try:
            stats = Stat(**(await get_player_info(name)))
            info_v3 = await get_player_info_v3(name)
        except ValidationError as e:
            logger.error(e)
            return "数据错误: API可能暂时无法访问或已更新"
    try:
        stats_variables = await get_stats_variables(stats, info_v3)
        if args.verbose:
            msg = player_stat_verbose.format(**stats_variables)
        else:
            msg = player_stat.format(**stats_variables)
        return msg
    except KeyError as e:
        logger.error(e)
        return "数据错误: API可能暂时无法访问或已更新"


async def handle_item(args: Namespace) -> str:
    return "数据错误: 此功能还未实现"


async def handle_uptime(args: Namespace) -> str:
    data = get_data()
    servers = args.server
    servers_with_stats: dict[str, dict[str, Any]] = {}
    msg: list[str] = []
    if not servers:
        servers = data["servers"]
    for s in servers:
        if not s.startswith("WC") and s != "YT" and s != "TEST":
            s = f"WC{s}"
        s = s.upper()
        servers_with_stats[s] = {}
        servers_with_stats[s]["uptime"] = (
            datetime.datetime.now()
            - datetime.datetime.fromisoformat(data["servers"][s]["timestarted"])
        ).seconds
        servers_with_stats[s]["soulpoint"] = 1200 - (
            (
                datetime.datetime.now()
                - datetime.datetime.fromisoformat(data["servers"][s]["timestarted"])
            ).seconds
            % 1200
        )
        if args.soulpoint:
            # sort the servers by soulpoint
            servers_with_stats = {
                k: v
                for k, v in sorted(
                    servers_with_stats.items(),
                    key=lambda item: item[1]["soulpoint"],
                    reverse=args.reverse,
                )
            }
        elif not args.normal:
            servers_with_stats = {
                k: v
                for k, v in sorted(
                    servers_with_stats.items(),
                    key=lambda item: item[1]["uptime"],
                    reverse=not args.reverse,
                )
            }
    for s in servers_with_stats:
        online = data["servers"][s]["online"]
        uptime = datetime.timedelta(seconds=servers_with_stats[s]["uptime"])
        spmin, spsec = divmod(servers_with_stats[s]["soulpoint"], 60)
        soulpointregen = str(spmin).rjust(2, "0") + ":" + str(spsec).rjust(2, "0")
        playerscount = data["servers"][s]["playerscount"]
        if online:
            msg.append(
                server_stat_verbose.format(
                    server=align(s, 4),
                    uptime=uptime,
                    soulpointregen=soulpointregen,
                    playerscount=playerscount,
                )
            )
    return "\n".join(msg).strip()


async def get_stats_variables(stats: Stat, info_v3: dict) -> dict:
    _data = stats.data[0]
    return {
        "name": _data.username,
        "rank": _data.meta.tag.value if _data.meta.tag and _data.meta.tag.value else "无",
        "guildname": _data.guild.name if _data.guild and _data.guild.name else "无",
        "guildrank": _data.guild.rank if _data.guild and _data.guild.name else "无",
        "time": datetime.datetime.fromtimestamp(stats.timestamp / 1000, tz=utc_tz)
        .astimezone(sh_tz)
        .strftime("%Y-%m-%d %H:%M:%S"),
        "firstjoin": dateparser.isoparse(_data.meta.firstJoin)
        .astimezone(sh_tz)
        .strftime("%Y-%m-%d %H:%M:%S"),
        "lastjoin": dateparser.isoparse(_data.meta.lastJoin)
        .astimezone(sh_tz)
        .strftime("%Y-%m-%d %H:%M:%S"),
        "logintimes": _data.global_.logins,
        "playtime": info_v3["meta"]["playtime"],
        # "chestfound": _data.global_.chestsFound,
        "chestfound": "API目前暂不提供此数据",
        "blockwalked": _data.global_.blocksWalked,
        "mobskilled": _data.global_.mobsKilled,
        "deaths": _data.global_.deaths,
        "totallevel": _data.global_.totalLevel.combined,
        "taskscompleted": sum([class_.quests.completed for class_ in _data.classes]),
        "dungeonscompleted": sum(
            [class_.dungeons.completed for class_ in _data.classes]
        ),
        "raidscompleted": sum([class_.raids.completed for class_ in _data.classes]),
        "discoveries": _data.global_.discoveries,
    }
