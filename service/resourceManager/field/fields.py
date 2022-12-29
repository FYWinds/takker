"""
Author       : FYWinds i@windis.cn
Date         : 2022-10-18 17:25:02
LastEditors  : FYWinds i@windis.cn
LastEditTime : 2022-10-22 10:54:21
FilePath     : /service/resourceManager/field/fields.py

Copyright (c) 2022 by FYWinds i@windis.cn
All Rights Reserved.
Any modifications or distributions of the file
should mark the original author's name.
"""

from typing import TextIO, BinaryIO, Optional

from service.resourceManager.field.base import BaseField, ResourceKey


class BinaryIOField(BaseField[BinaryIO]):
    def __init__(
        self,
        key: str | ResourceKey,
        default: Optional[BinaryIO] = None,
        nullable=False,
        description: Optional[str] = None,
    ) -> None:
        super().__init__(key, default, nullable, description)

    def init(self) -> None:
        self.value = self.key.to_path().open("rb")

    @property
    def value(self) -> Optional[BinaryIO]:
        if self.value is None:
            self.init()
        return self.value

    @value.setter
    def value(self, value: Optional[BinaryIO]) -> None:
        self.value = value
        if value is not None:
            self.key.to_path().write_bytes(value.read())

    @value.deleter
    def value(self) -> None:
        if self.value:
            self.value.close()
            self.value = None


class TextIOField(BaseField[TextIO]):
    def __init__(
        self,
        key: str | ResourceKey,
        default: Optional[TextIO] = None,
        nullable=False,
        description: Optional[str] = None,
    ) -> None:
        super().__init__(key, default, nullable, description)

    def init(self) -> None:
        self.value = self.key.to_path().open("r")

    @property
    def value(self) -> Optional[TextIO]:
        if self.value is None:
            self.init()
        return self.value

    @value.setter
    def value(self, value: Optional[TextIO]) -> None:
        self.value = value
        if value is not None:
            self.key.to_path().write_text(value.read())

    @value.deleter
    def value(self) -> None:
        if self.value:
            self.value.close()
            self.value = None
