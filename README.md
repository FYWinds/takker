[![Time](https://wakatime.com/badge/github/FYWinds/takker.svg)](https://wakatime.com/badge/github/FYWinds/takker)

![maven](https://img.shields.io/badge/python-3.9%2B-green)
![maven](https://img.shields.io/badge/nonebot-2.0.0a15-mint)
![maven](https://img.shields.io/badge/go--cqhttp-1.0.0--beta6-lime)

# Takker 目前还没啥功能（
# 且没经过完整测试，一定有一堆bug
****
## 此项目基于 Nonebot2 和 go-cqhttp 开发，以 Sqlite 作为数据库的QQ群娱乐机器人

## 关于
纯兴趣开发，部分功能借鉴了大佬们的代码，作为Q群的娱乐+功能性Bot

## 声明
此项目仅用于学习交流，请勿用于非法用途

## 帮助
待完善


## 功能列表
<details>
<summary>已实现的功能</summary>

### 已实现的常用功能
- [x] 每日一签
- [x] pixiv美图/色图 (常用(大嘘
- [x] 缩写查询
- [x] 群内消息总结（每月/每年）
- [x] 一言
- [x] 插件调用统计
- [x] xp统计
- [x] 傲娇钉宫语音包

### 已实现的管理员功能
- [x] 95%的插件功能开关 (基于[nonebot_plugin_manager](https://github.com/Jigsaw111/nonebot_plugin_manager)插件修改)

### 已实现的超级用户功能
- [x] 添加/删除管理（实际上就是设置用户权限）
- [x] 修改群权限
- [x] 多群公告
  
#### 超级用户的被动技能
- [x] 好友请求转发给主人处理
- [x] 超级用户发送多群联合公告后通知主人

### 已实现的被动技能
- [x] 被超级用户拉入群聊自动通过
- [x] 复读
- [x] 问（智障回复）

### 已实现的隐藏技能！
- [x] 检测恶意触发命令（将被次高权限ban掉5分钟，只有最高权限(9&10级)可以进行unban）
- [x] 群权限系统
  </details>

## 功能具体指令
<details>
<summary>功能具体指令说明</summary>

### 常用功能
参数范例: [必填参数] <可选参数>

功能         | 指令              | 说明                                                                                         | 权限
|:----------:|:-----------------|:--------------------------------------------------------------------------------------------|:--:|
|每日一签     | 签到/luck/抽签/运势| 发送后返回一张图片，包含随机acg美图、日期、今日运势                                                 | 1  |
|权限系统     | perm get</br>perm set [权限等级]| 获取当前对话的权限等级</br>设置当前会话的权限等级                                     | >权限等级|
|pixiv美图/色图| pix <关键词> <-l NSFW等级> | 获得一张pixiv的美图、图片信息和图片的高清链接！                                           | 6  |
| 问         | 以问开头的语句自动触发| 匹配句中的x不x，多少，多久，什么时候，谁 进行人工智障的回答                                          | 1 |
| 缩写查询    | 好好说话 [缩写]     | 返回查询到的可能代表的内容（接口[magiconch](https://lab.magiconch.com/api/nbnhhsh/guess)）       | 2  |
| 群内消息总结 | 本群月内总结/本群年内总结| 效果见功能展示                                                                             | 消息记录权限 1 </br> 调用生成总结权限 群管理员+超级用户 |
| 复读        | 相同的三条消息后自动触发| ?这都需要说明吗                                                                            | 2  |
| 一言        | .h <类型>          | a 动画 b 文学 c 影视 d 诗词 e 哲学 f 网易云                                                    | 1  |
| 亲亲GIF     | 亲@目标            | 生成一张狂亲的GIF                                                                            | 2  |
| 摸头GIF     | 摸@目标            | 生成一张摸头的GIF                                                                            | 2  |
| 点歌        | 点歌 歌名           | 顾名思义                                                                                    | 2  |
| 插件调用统计  | 插件调用统计        | 生成一张统计图片                                                                             | 2  |
| xp统计      | xp统计             | 生成一张统计图片，数据源为illust插件搜索的关键词                                                  | 2  |
| 钉宫语音包   | 傲娇               | 发送一条钉宫的语音和对应的中文翻译                                                               | 3  |

### 管理员功能
功能         | 指令              | 说明                                                                                         | 权限
|:----------:|:-----------------|:--------------------------------------------------------------------------------------------|:--:|
| 插件管理器   | pm list/ban/unban| pm list获取当前会话插件列表</br>pm ban/unban [插件1] <插件x> 禁用/启用当前会话的指定插件             | 群管理员+超级用户|

### 超级用户功能
功能         | 指令              | 说明                                                                                         | 权限
|:----------:|:-----------------|:--------------------------------------------------------------------------------------------|:--:|
| 多群联合公告 | notice [群1 群2] -n [公告内容]| 以1-2秒的随机间隔依次向指定群聊发送一条公告，公告内容暂不支持换行                          | 9  |
|权限系统     | perm list</br>perm set [权限等级] <-g 群号>/<-u qq号>| 获取加入的所有群聊的权限等级</br>设置指定群聊/用户的权限等级       | SUPERUSERS|

</details>

## 部分功能展示
<details>
<summary>功能实例展示</summary>

### 群内消息总结词云
![](https://raw.githubusercontent.com/FYWinds/takker/master/docs/img/summary_wordcloud.png)

</details>

## 配置文件注解
<details>
<summary>各配置文件说明</summary>

./configs/config.py

```python
# Go-cq正向http地址配置(默认使用bot.call_api()的调用方式)
USE_HTTP_API: bool = False
CQ_HTTP_URL: str = ""
CQ_SECRET: str = ""  # HTTP_API的secret

# 身份名单
OWNER: str = ""  # 主人
SUPERUSERS: List[str] = ["0", "", ""]  # 超级用户名单

# 各个API的配置
ALAPI_TOKEN: str = ""  # ALAPI
CATAPI_TOKEN: str = ""  # 随机猫猫API
NETEASE_API: str = ""  # NodeJS版本的网易云音乐API的地址
PIXIV_IMAGE_URL: str = ""  # 反代i.pximg.net的网址

# 各种限制
MAX_PROCESS_TIME: int = 30  # 部分指令处理最大等待时间，单位秒，在此期间用户不能再次发起相同指令
BAN_CHEKC_FREQ: int = 5  # 恶意触发命令检测阈值
BAN_CHECK_PERIOD: int = 3  # 恶意触发命令检测时间
BAN_TIME: int = 5  # 恶意触发命令后的封禁时间，单位分钟

# 隐藏插件列表
HIDDEN_PLUGINS: List[str] = [
    "nonebot_plugin_apscheduler",
    "nonebot_plugin_test",
    "hook",
    "invite_check",
]
```

./configs/path_config.py

```python
# 图片路径
IMAGE_PATH = Path("resources/img/")
# 音频路径
VOICE_PATH = Path("resources/voice/")
# 文本路径
TEXT_PATH = Path("resources/text/")
# 模板路径
TEMPLATE_PATH = Path("resources/templates")
# 字体路径
FONT_PATH = Path("resources/fonts/")
# 日志路径
LOG_PATH = Path("log/")
# 数据路径
DATA_PATH = Path("data/")
# 临时图片路径
TEMP_PATH = Path("resources/img/temp/")
```
</details>


## 更新记录

### 2021/8/21
* 修复每日签到积分bug
* 修复部分插件权限问题
* 添加了钉宫语音包功能
* 修复插件管理器获取权限报错的问题
* 修复了私聊bot设置自己权限时报错无反馈的问题


### 2021/8/20
* 修复一些优先级的bug
* 加入插件统计
* 加入xp统计
* 修复一些绘图BUG
* 加入所有环境下都关闭重载
* 修复不知道哪些BUG
* 修改pixiv美图发送的图片质量和链接内容

### 2021.8.19
* 修了一整天的服务器，现在bot内部调用的我自建的API都正常了
* 修复插件管理系统禁用插件时的bug
* 修复权限和插件管理的-u -g不能同时管理多个会话的bug
* 修复pixiv美图功能若原画失效导致抛出Exception的bug
* 修复公告插件无法发送多行公告
* 更新部分依赖

### 2021/8/18
* 点歌、摸头GIF、狂亲GIF
* Legacy插件重构完成
* 配置文件更新为空配置，需手动修改

### 2021/8/17
* 又是很多神奇的东西
* Legacy的插件基本要重置完成了

### 2021/8/16
* 很多神奇的东西（懒得写了

### 2021/8/15
* 智障随机问答

### 2021/8/14
* pixiv美图

### 2021/8/13
* 加入了多群联合公告插件
* 在README中对部分功能进行了说明
* 更新到光速发版的nonebot 2.0.0a15

### 2021/8/12
* 加入签到插件(至少能用了(有功能辣！))

### 2021/7/31
* 数据库相关服务和模型

### 2021/7/29
* 开始重构Takker(指新建文件夹)
* 重新封装部分API


## Todo
- [ ] 群管功能
- [ ] 缓存清理功能
- [ ] docker容器化部署
- [ ] Web管理面板
- [ ] 完善各种功能
- [ ] 提供非侵入式的权限等级管理方式
- [ ] 提供非侵入式的帮助菜单

## 感谢
[Onebot](https://github.com/howmanybots/onebot)  
[go-cqhttp](https://github.com/Mrs4s/go-cqhttp)  
[nonebot2](https://github.com/nonebot/nonebot2)  
[zhenxun_bot](https://github.com/HibiKier/zhenxun_bot)  
[nonebot_plugin_songpicker2](https://github.com/maxesisn/nonebot_plugin_songpicker2)    
[nonebot_plugin_manager](https://github.com/Jigsaw111/nonebot_plugin_manager)  
[saya_plugin_collection](https://github.com/SAGIRI-kawaii/saya_plugins_collection)  
[nonebot_plugin_help](https://github.com/XZhouQD/nonebot-plugin-help)  
