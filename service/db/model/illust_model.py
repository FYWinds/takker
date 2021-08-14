"""
Author: FYWindIsland
Date: 2021-08-13 16:41:49
LastEditTime: 2021-08-13 16:41:51
LastEditors: FYWindIsland
Description: 
I'm writing SHIT codes
"""
"""
Author: FYWindIsland
Date: 2021-08-13 14:55:43
LastEditTime: 2021-08-13 15:09:16
LastEditors: FYWindIsland
Description: 
I'm writing SHIT codes
"""
from tortoise.models import Model
from tortoise.fields.data import IntField, BooleanField, TextField


class Illust(Model):
    """图库"""

    id = IntField(pk=True)
    pid = IntField()
    uid = IntField()
    title = TextField()
    author = TextField()
    nsfw = IntField()
    tags = TextField()
    url = TextField()
    width = IntField()
    height = IntField()

    class Meta:
        table = "pixiv"
        table_description = "色图数据"
