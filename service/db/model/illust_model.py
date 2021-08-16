"""
Author: FYWindIsland
Date: 2021-08-13 16:41:49
LastEditTime: 2021-08-14 20:51:01
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
