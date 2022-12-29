"""
Author       : FYWinds i@windis.cn
Date         : 2022-10-17 10:59:27
LastEditors  : FYWinds i@windis.cn
LastEditTime : 2022-10-21 13:51:45
FilePath     : /service/resourceManager/model.py

Copyright (c) 2022 by FYWinds i@windis.cn
All Rights Reserved.
Any modifications or distributions of the file
should mark the original author's name.
"""

from service.resourceManager.field import BaseField, ResourceKey


class MetaResourceModel(type):
    """
    :说明: `MetaResourceModel`
    > 资源模型
    """

    def __new__(cls, name, bases, attrs: dict) -> "MetaResourceModel":
        baseKey: ResourceKey = ResourceKey(name)  # for futher key tree resolve
        for name, field in attrs.items():
            if name == "__resourceKey__":
                if isinstance(field, ResourceKey):
                    baseKey = field
                elif isinstance(field, str):
                    baseKey = ResourceKey(field)
                else:
                    raise TypeError(
                        f"BaseResourceKey must be `ResourceKey` or `str`, not {field.__class__.__name__}"
                    )

            if isinstance(field, BaseField):
                if not baseKey:
                    raise ValueError("Missing BaseResourceKey")
                field.setKey(baseKey + field.key)
                field.init()

        # TODO Schedule the key auto remove in the future
        return super().__new__(cls, name, bases, attrs)
