![maven](https://img.shields.io/badge/python-3.9%2B-blue)
![maven](https://img.shields.io/badge/nonebot-2.0.0-green)
![maven](https://img.shields.io/badge/go--cqhttp-1.0.0--beta4-purple)

# Takker 目前还没啥功能（
# 且没经过完整测试，一定有一堆bug
****
此项目基于 Nonebot2 和 go-cqhttp 开发，以 Sqlite 作为数据库的QQ群娱乐机器人

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
- [x] 每日签到

### 已实现的管理员功能
- [x] 95%的插件功能开关 (基于[nonebot_plugin_manager](https://github.com/Jigsaw111/nonebot_plugin_manager)插件修改)

### 已实现的超级用户功能
- [x] 添加/删除管理（实际上就是设置用户权限）
- [x] 修改群权限
  
#### 超级用户的被动技能
- [x] 待完善

### 已实现的被动技能
- [ ] 待完善

### 已实现的隐藏技能！
- [x] 检测恶意触发命令（将被次高权限ban掉5分钟，只有最高权限(9&10级)可以进行unban）
- [x] 群权限系统
</details>

## 功能具体指令
<details>
<summary>功能具体指令说明</summary>

### 常用功能

### 管理员功能

### 超级用户功能

</details>

## 部分功能展示
<details>
<summary>功能实例展示</summary>
</details>

## 配置文件注解
<details>
<summary>各配置文件说明</summary>
./configs/config.py

```
待完善
```
</details>


## 更新记录

### 2021/8/12
* 加入签到插件(至少能用了(有功能辣！))

### 2021/7/31
* 数据库相关服务和模型

### 2021/7/29
* 开始重构Takker(指新建文件夹)
* 重新封装部分API


## Todo
- [ ] 重构原先插件
- [ ] 提供更多对插件的控制
- [ ] 群管功能
- [ ] 缓存清理功能
- [ ] docker容器化部署
- [ ] Web管理面板
- [ ] 完善各种功能

## 感谢
[Onebot](https://github.com/howmanybots/onebot)  
[go-cqhttp](https://github.com/Mrs4s/go-cqhttp)  
[nonebot2](https://github.com/nonebot/nonebot2)  
[zhenxun_bot](https://github.com/HibiKier/zhenxun_bot)  
[nonebot_plugin_songpicker2](https://github.com/maxesisn/nonebot_plugin_songpicker2)    
[nonebot_plugin_manager](https://github.com/Jigsaw111/nonebot_plugin_manager)  
[saya_plugin_collection](https://github.com/SAGIRI-kawaii/saya_plugins_collection)  
[nonebot_plugin_help](https://github.com/XZhouQD/nonebot-plugin-help)  
