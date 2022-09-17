import httpx
import nonebot
from nonebot.plugin import on_command
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import Bot, MessageEvent

from utils.rule import limit_group
from utils.img_util import textToImageBuf
from utils.msg_util import image
from utils.text_util import align

__plugin_info__ = {
    "name": "Wynndata-Guild",
    "des": "Wynncraft公会数据查询",
    "usage": {
        "/guild <name>": "查询指定公会在线情况",
    },
    "author": "风屿",
    "version": "1.5.0",
    "permission": 3,
}

driver = nonebot.get_driver()


guild = on_command(
    "/guild",
    aliases={".guild"},
    priority=20,
    block=True,
    rule=limit_group([521656488, 878663967]),
)


@guild.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    guildname = str(event.get_plaintext())
    if guildname == "":
        guildname = "ChinaNumberOne"
    if guildname.upper() in prefix_toName.keys():
        guildname = prefix_toName[guildname.upper()]
    guildinfo = await getGuildInfo(guildname)

    members = guildinfo["members"]
    owner = members["OWNER"]
    owner_name = next(iter(owner))
    owner_online = owner[owner_name]["location"]["online"]
    owner_server = owner[owner_name]["location"]["server"]

    CHIEF_list = {}
    for player in members["CHIEF"]:
        if members["CHIEF"][player]["location"]["online"]:
            CHIEF_list[player] = members["CHIEF"][player]["location"]["server"]

    STRATEGIST_list = {}
    for player in members["STRATEGIST"]:
        if members["STRATEGIST"][player]["location"]["online"]:
            STRATEGIST_list[player] = members["STRATEGIST"][player]["location"]["server"]

    CAPTAIN_list = {}
    for player in members["CAPTAIN"]:
        if members["CAPTAIN"][player]["location"]["online"]:
            CAPTAIN_list[player] = members["CAPTAIN"][player]["location"]["server"]

    RECRUITER_list = {}
    for player in members["RECRUITER"]:
        if members["RECRUITER"][player]["location"]["online"]:
            RECRUITER_list[player] = members["RECRUITER"][player]["location"]["server"]

    RECRUIT_list = {}
    for player in members["RECRUIT"]:
        if members["RECRUIT"][player]["location"]["online"]:
            RECRUIT_list[player] = members["RECRUIT"][player]["location"]["server"]

    msg = template.format(
        name=guildinfo["name"],
        short_name=guildinfo["prefix"],
        online_players=guildinfo["onlineMembers"],
        total_players=guildinfo["totalMembers"],
        owner=f"{owner_name} {owner_server if owner_online else '离线'}",
        chief="\n".join([f"{align(x, 27)}{CHIEF_list[x]}" for x in CHIEF_list])
        if CHIEF_list
        else "无在线成员",
        strategist="\n".join(
            [f"{align(x, 27)}{STRATEGIST_list[x]}" for x in STRATEGIST_list]
        )
        if STRATEGIST_list
        else "无在线成员",
        captain="\n".join([f"{align(x, 27)}{CAPTAIN_list[x]}" for x in CAPTAIN_list])
        if CAPTAIN_list
        else "无在线成员",
        recruiter="\n".join(
            [f"{align(x, 27)}{RECRUITER_list[x]}" for x in RECRUITER_list]
        )
        if RECRUITER_list
        else "无在线成员",
        recruit="\n".join([f"{align(x, 27)}{RECRUIT_list[x]}" for x in RECRUIT_list])
        if RECRUIT_list
        else "无在线成员",
    )
    await bot.send(event, image(c=await textToImageBuf(msg, cut=0)))


async def getGuildInfo(name: str) -> dict:
    async with httpx.AsyncClient() as client:
        r = await client.get(f"https://wynn.windis.cn/v3/guild/{name}")
    return r.json()


guild_xp = on_command(
    "/guildxp",
    aliases={".guildxp"},
    priority=20,
    block=True,
    rule=limit_group([521656488, 878663967]),
)


@guild_xp.handle()
async def __(bot: Bot, event: MessageEvent, state: T_State):
    guildname = str(event.get_plaintext())
    if guildname == "":
        guildname = "ChinaNumberOne"
    if guildname.upper() in prefix_toName.keys():
        guildname = prefix_toName[guildname.upper()]
    guildinfo = await getGuildInfo(guildname)

    owner_name: str = next(iter(guildinfo["members"]["OWNER"]))
    owner: dict[str, str] = {
        owner_name: human_format(
            guildinfo["members"]["OWNER"][owner_name]["contributed"]
        )
    }
    members: dict[str, str] = {}

    for stage in guildinfo["members"]:
        if state == "OWNER":
            continue
        for player in guildinfo["members"][stage]:
            members[player] = guildinfo["members"][stage][player]["contributed"]

    top20 = sorted(members.items(), key=lambda x: x[1], reverse=True)[:20]

    msg = template_xp.format(
        name=guildname,
        short_name=guildinfo["prefix"],
        online_players=guildinfo["onlineMembers"],
        total_players=guildinfo["totalMembers"],
        owner=f"{owner_name} {owner[owner_name]}",
        top20="\n".join([f"{align(x[0], 27)}{human_format((x[1]))}" for x in top20]),
    )
    await bot.send(event, image(c=await textToImageBuf(msg, cut=0)))


def human_format(num):
    num = float("{:.3g}".format(num))
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    return "{}{}".format(
        "{:f}".format(num).rstrip("0").rstrip("."), ["", "K", "M", "B", "T"][magnitude]
    )


template = """
公会名称: {name} - {short_name}
在线玩家: {online_players}/{total_players}
所有者: {owner}
------------ CHIEF ------------
{chief}
---------- STRATEGIST ---------
{strategist}
----------- CAPTAIN -----------
{captain}
---------- RECRUITER ----------
{recruiter}
----------- RECRUIT -----------
{recruit}
""".strip()

template_xp = """
公会名称: {name} - {short_name}
在线玩家: {online_players}/{total_players}
所有者: {owner}
------------ 贡献度 ------------
{top20}
""".strip()

prefix_toName = {
    "AVO": "Avicia",
    "ANO": "Titans Valor",
    "DUDE": "KongoBoys",
    "AEQ": "Aequitas",
    "TAQ": "The Aquarium",
    "BLA": "Blacklisted",
    "NFR": "Nefarious Ravens",
    "FOX": "Kingdom Foxes",
    "ESI": "Empire of Sindria",
    "SDU": "Sins of Seedia",
    "MALD": "The Clowns",
    "WNLY": "Wynn Legacy",
    "IBT": "IceBlue Team",
    "PROF": "Profession Heaven",
    "GKS": "Gopniks",
    "PUN": "Paladins United",
    "ERN": "Emorians",
    "NIA": "Nerfuria",
    "SHY": "ShadowFall",
    "TNL": "TheNoLifes",
    "HAX": "HackForums",
    "LXA": "Lux Nova",
    "MAG": "The Mage Legacy",
    "ILQ": "The Simple Ones",
    "FUY": "busted moments",
    "EDN": "Eden",
    "GSW": "Guardian of Wynn",
    "ICO": "Idiot Co",
    "TBGM": "The Broken Gasmask",
    "IMP": "Imperial",
    "WFN": "Wheres The Finish",
    "TSD": "TruthSworD",
    "ASH": "Achte Shadow",
    "FUX": "Fantasy",
    "GBE": "Gabameno",
    "DDT": "DiamondDeities",
    "WOOD": "The Forest",
    "CNM": "ChinaNumberOne",
    "OCE": "Wrath Of Poseidon",
    "BRIS": "BRIS",
    "PHI": "Phantom Hearts",
    "AIN": "Atlas Inc",
    "TNI": "The Dark Phoenix",
    "DEU": "Germany",
    "OXO": "Roses",
    "LBL": "LittleBunny Land",
    "FXX": "Forever Twilight",
    "WFA": "WrathOfTheFallen",
    "RAYS": "Ultra Violet",
    "ALTS": "Alternate Accounts",
    "FOOL": "Gang of Fools",
    "GMY": "Germany Elite",
    "CXZ": "Fuzzy Spiders",
    "WNI": "Winds of Nigh",
    "PZE": "Periodic Table",
    "MIN": "Minerva",
    "THI": "The Hive",
    "VNP": "TVietNam",
    "FEU": "SICA Team",
    "APA": "Astrum Pantheon",
    "SPC": "Spectral Cabbage",
    "MDM": "GlowOfDust",
    "NUGS": "Nuggets",
    "JSON": "JavaScript Object Notation",
    "UXS": "UltimateXeons",
    "FKL": "ForsakenLaws",
    "IPS": "Last Order",
    "CONA": "Crystal Iris",
    "OPM": "Opus Maximus",
    "KYN": "Skyborn",
    "PAIN": "La League Des Baguettes",
    "FATE": "Tartarus Wrath",
    "LEAF": "Jasmine Dragon",
    "WTH": "Wynn Theory",
    "BCR": "BuildCraftia",
    "RZL": "Roselia",
    "OUS": "RedLotus",
    "KAE": "Ikea Sharks",
    "WFT": "WynnFairyTail",
    "GSB": "BlueStoneGroup",
    "DXI": "Diablo",
    "BSE": "Breadskate",
    "PED": "Woodpeckers",
    "EXIL": "Banished",
    "LMDR": "LaMafiaDeRagni",
    "FLK": "FlameKnights",
    "VMZ": "Vindicator",
    "YIN": "The Farplane",
    "CYX": "Cyphrus Code",
    "HICH": "ironman btw",
    "FESH": "jellyfishe",
    "UTL": "TerraLune",
    "REA": "Renegade",
    "SDY": "ShadowedSerenity",
    "CDR": "Caeruleum Order",
    "HSP": "Hesperides",
    "JPPF": "Japanese Proffers",
    "AVOS": "the Avos",
    "LOVE": "Heartbreakers",
    "JEUS": "Jeus",
}
