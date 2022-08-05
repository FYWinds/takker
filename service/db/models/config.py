from tortoise.models import Model
from tortoise.fields.data import IntField, CharField, JSONField, BigIntField

#! 机器人数据库结构版本号 请勿随意修改，否则造成数据混乱甚至丢失概不负责
VERSION_TAG: str = "1.1.0"  #! 在机器人更新版本，重启后自动检测并更新
#! 自动检测更新需要确保config.example.py为最新版且存在于configs目录下


class UserConfig(Model):
    """用户配置"""

    uid = BigIntField(pk=True)
    points = BigIntField(null=True)
    constellation = IntField(null=True)
    perm = IntField(null=True)
    plugin_status = JSONField(null=True)

    class Meta:
        table = "user_config"
        table_description = "用户配置数据"
        indexes = ("uid",)


class GroupConfig(Model):
    """群组配置"""

    gid = BigIntField(pk=True)
    perm = IntField(null=True)
    plugin_status = JSONField(null=True)

    class Meta:
        table = "group_config"
        table_description = "群组配置数据"
        indexes = ("gid",)


class BotConfig(Model):
    """机器人全局配置内容"""

    version = CharField(max_length=32)
    illust_config = JSONField(null=True)

    class Meta:
        table = "bot_config"
        table_description = "机器人全局配置内容，部分关键字段请勿随意修改"
