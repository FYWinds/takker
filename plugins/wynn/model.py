# generated by datamodel-codegen:
#   filename:  stat_example.json
#   timestamp: 2022-05-17T03:14:48+00:00

from __future__ import annotations

from typing import Any, List, Optional

from pydantic import Field, BaseModel


class Location(BaseModel):
    online: bool
    server: Any


class Tag(BaseModel):
    display: bool
    value: Optional[str] = None


class Meta(BaseModel):
    firstJoin: str
    lastJoin: str
    location: Location
    playtime: int
    tag: Tag
    veteran: bool


class ListItem(BaseModel):
    name: str
    completed: int


class Dungeons(BaseModel):
    completed: int
    list: List[ListItem]


class ListItem1(BaseModel):
    name: str
    completed: int


class Raids(BaseModel):
    completed: int
    list: List[ListItem1]


class Quests(BaseModel):
    completed: int
    list: List[str]


class Pvp(BaseModel):
    kills: int
    deaths: int


class Gamemode(BaseModel):
    craftsman: bool
    hardcore: bool
    ironman: bool
    hunted: bool


class Skills(BaseModel):
    strength: int
    dexterity: int
    intelligence: int
    defence: int
    defense: int
    agility: int


class Alchemism(BaseModel):
    level: Optional[int] = 0
    xp: Optional[float] = 0


class Armouring(BaseModel):
    level: Optional[int] = 0
    xp: Optional[float] = 0


class Combat(BaseModel):
    level: Optional[int] = 0
    xp: Optional[float] = 0


class Cooking(BaseModel):
    level: Optional[int] = 0
    xp: Optional[float] = 0


class Farming(BaseModel):
    level: Optional[int] = 0
    xp: Optional[float] = 0


class Fishing(BaseModel):
    level: Optional[int] = 0
    xp: Optional[float] = 0


class Jeweling(BaseModel):
    level: Optional[int] = 0
    xp: Optional[float] = 0


class Mining(BaseModel):
    level: Optional[int] = 0
    xp: Optional[float] = 0


class Scribing(BaseModel):
    level: Optional[int] = 0
    xp: Optional[float] = 0


class Tailoring(BaseModel):
    level: Optional[int] = 0
    xp: Optional[float] = 0


class Weaponsmithing(BaseModel):
    level: Optional[int] = 0
    xp: Optional[float] = 0


class Woodcutting(BaseModel):
    level: Optional[int] = 0
    xp: Optional[float] = 0


class Woodworking(BaseModel):
    level: Optional[int] = 0
    xp: Optional[float] = 0


class Professions(BaseModel):
    alchemism: Alchemism
    armouring: Armouring
    combat: Combat
    cooking: Cooking
    farming: Farming
    fishing: Fishing
    jeweling: Jeweling
    mining: Mining
    scribing: Scribing
    tailoring: Tailoring
    weaponsmithing: Weaponsmithing
    woodcutting: Woodcutting
    woodworking: Woodworking


class Class(BaseModel):
    name: str
    level: Optional[int] = 0
    dungeons: Dungeons
    raids: Raids
    quests: Quests
    itemsIdentified: int
    mobsKilled: int
    pvp: Pvp
    # chestsFound: int
    blocksWalked: int
    logins: int
    deaths: int
    playtime: int
    gamemode: Gamemode
    skills: Skills
    professions: Professions
    discoveries: int
    eventsWon: int
    preEconomyUpdate: bool


class Guild(BaseModel):
    name: Optional[str] = None
    rank: Optional[str] = None


class TotalLevel(BaseModel):
    combat: int
    profession: int
    combined: int


class Pvp1(BaseModel):
    kills: int
    deaths: int


class Global(BaseModel):
    # chestsFound: int
    blocksWalked: int
    itemsIdentified: int
    mobsKilled: int
    totalLevel: TotalLevel
    pvp: Pvp1
    logins: int
    deaths: int
    discoveries: int
    eventsWon: int


class Solo(BaseModel):
    combat: Any
    woodcutting: Any
    mining: Any
    fishing: Any
    farming: Any
    alchemism: Any
    armouring: Any
    cooking: Any
    jeweling: Any
    scribing: Any
    tailoring: Any
    weaponsmithing: Any
    woodworking: Any
    profession: Any
    overall: Any


class Overall(BaseModel):
    all: Any
    combat: Any
    profession: Any


class Player(BaseModel):
    solo: Solo
    overall: Overall


class Ranking(BaseModel):
    guild: Any
    player: Player
    pvp: Any


class Datum(BaseModel):
    username: str
    uuid: str
    rank: Optional[str] = None
    meta: Meta
    classes: List[Class]
    guild: Optional[Guild] = None
    global_: Global = Field(..., alias="global")
    ranking: Ranking


class Stat(BaseModel):
    kind: str
    code: int
    timestamp: int
    version: str
    data: List[Datum]