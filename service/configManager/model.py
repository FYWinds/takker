"""
Author       : FYWinds i@windis.cn
Date         : 2022-10-17 10:59:27
LastEditors  : FYWinds i@windis.cn
LastEditTime : 2022-11-30 11:39:06
FilePath     : /service/configManager/model.py

Copyright (c) 2022 by FYWinds i@windis.cn
All Rights Reserved.
Any modifications or distributions of the file
should mark the original author's name.
"""

from .field import BaseField, ConfigKey


class MetaConfigModel(type):
    """
    :说明: `MetaConfigModel`
    > 资源模型
    """

    def __new__(cls, name, bases, attrs: dict) -> "MetaConfigModel":
        baseKey: ConfigKey = ConfigKey(name)  # for futher key tree resolve
        for name, field in attrs.items():
            if name == "__configKey__":
                if isinstance(field, ConfigKey):
                    baseKey = field
                elif isinstance(field, str):
                    baseKey = ConfigKey(field)
                else:
                    raise TypeError(
                        f"BaseConfigKey must be `ConfigKey` or `str`, not {field.__class__.__name__}"
                    )

            if isinstance(field, BaseField):
                if not baseKey:
                    raise ValueError("Missing BaseConfigKey")
                field.setKey(baseKey + field.key)
                field.init()

        # TODO Schedule the key auto remove in the future
        return super().__new__(cls, name, bases, attrs)
