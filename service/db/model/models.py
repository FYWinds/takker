from typing import Text
from tortoise.models import Model
from tortoise.fields.data import *  # type: ignore


class Starluck(Model):
    """星座运势"""

    uid = BigIntField(pk=True)
    star = IntField()

    class Meta:
        table = "star"
        table_description = "星座运势绑定数据"


class Permission(Model):
    """权限系统"""

    id = TextField(pk=True)
    perm = IntField()

    class Meta:
        table = "permission"
        table_description = "权限系统数据"


class Ban(Model):
    """封禁系统"""

    uid = BigIntField(pk=True)
    ban_level = IntField()
    ban_time = BigIntField()
    duration = BigIntField()

    class Meta:
        table = "ban"
        table_description = "封禁系统数据"


class Plugin(Model):
    """插件管理器
    由于插件变动较为频繁
    选择将插件数据以text形式存储"""

    id = TextField(pk=True)
    status = TextField(null=True)

    class Meta:
        table = "plugin_manager"
        table_description = "插件管理器数据"


class Wordcloud(Model):
    """群热词词云"""

    gid = BigIntField()
    uid = BigIntField()
    time = BigIntField()
    msg = TextField(null=True)
    msg_seg = TextField(null=True)

    class Meta:
        table = "wordcloud"
        table_description = "热词词云数据"


class Point(Model):
    """游戏积分"""

    uid = BigIntField(pk=True)
    points = BigIntField()

    class Meta:
        table = "point"
        table_description = "机器人积分系统数据"


class Statistic(Model):
    """插件调用数据"""

    gid = BigIntField(pk=True)
    stat = TextField(null=True)
    illust_stat = TextField(null=True)

    class Meta:
        table = "statistic"
        table_description = "插件调用数据"
