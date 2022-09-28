player_stat: str = """玩家: {name} {rank}
所属工会: {guildname} - {guildrank}
信息获取时间: {time}

上次登录: {lastjoin}
总游玩时长: {playtime} 小时
已开启宝箱数: {chestfound}
已击杀怪物数: {mobskilled}"""

player_stat_verbose: str = """玩家: {name} {rank}
所属工会: {guildname} - {guildrank}
信息获取时间: {time}

首次登录: {firstjoin}
上次登录: {lastjoin}
登录次数: {logintimes}
总游玩时长: {playtime} 小时
已开启宝箱数: {chestfound}
走过的距离: {blockwalked}
已击杀怪物数: {mobskilled}
死亡次数: {deaths}

以下为所有角色总计
等级: {totallevel}
完成任务: {taskscompleted}
完成地牢次数: {dungeonscompleted}
完成突袭次数: {raidscompleted}
探索发现: {discoveries}"""

item_stat: str = ""

item_stat_verbose: str = ""

server_stat: str = """服务器: {server} 是否开启: {online}   开启时长: {uptime}"""

server_stat_verbose: str = (
    """服务器: {server} 开启时长: {uptime}  离灵魂点恢复还有: {soulpointregen}  在线玩家: {playerscount}"""
)
