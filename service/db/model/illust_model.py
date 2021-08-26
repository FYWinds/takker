from tortoise.models import Model
from tortoise.fields.data import IntField, BooleanField, TextField


class Illust(Model):
    """图库"""

    pid = IntField(pk=True)
    uid = IntField()
    nsfw = IntField()
    title = TextField()
    author = TextField()
    tags = TextField()
    url = TextField()

    class Meta:
        table = "pixiv"
        table_description = "色图数据"
