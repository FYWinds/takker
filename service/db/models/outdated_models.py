from tortoise.models import Model
from tortoise.fields.data import *  # type: ignore


class Starluck(Model):
    """星座运势
    已过时"""

    uid = BigIntField(pk=True)
    star = IntField()

    class Meta:
        table = "star"
        table_description = "星座运势绑定数据"


class Permission(Model):
    """权限系统
    已过时"""

    id = TextField(pk=True)
    perm = IntField()

    class Meta:
        table = "permission"
        table_description = "权限系统数据"


class Point(Model):
    """游戏积分
    已过时"""

    uid = BigIntField(pk=True)
    points = BigIntField()

    class Meta:
        table = "point"
        table_description = "机器人积分系统数据"


class Plugin(Model):
    """插件管理器
    已过时"""

    id = TextField(pk=True)
    status = TextField(null=True)

    class Meta:
        table = "plugin_manager"
        table_description = "插件管理器数据"

