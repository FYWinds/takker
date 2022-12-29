"""
Author       : FYWinds i@windis.cn
Date         : 2022-10-18 14:49:14
LastEditors  : FYWinds i@windis.cn
LastEditTime : 2022-10-21 13:46:48
FilePath     : /service/resourceManager/field/base.py

Copyright (c) 2022 by FYWinds i@windis.cn
All Rights Reserved.
Any modifications or distributions of the file
should mark the original author's name.
"""
import warnings
from typing import Any, Generic, TypeVar, Optional
from pathlib import Path

T_Value = TypeVar("T_Value", bound=Any)
SEPERATOR = "."


class ResourceKey:
    key: str

    def __init__(self, key: str):
        self.key = key

    def to_path(self) -> Path:
        return Path(self.key.replace(SEPERATOR, "/"))

    def __str__(self) -> str:
        return self.key

    def __repr__(self) -> str:
        return self.key

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, ResourceKey):
            return self.key == __o.key
        elif isinstance(__o, str):
            return self.key == __o
        return False

    def __add__(self, __o: str | "ResourceKey") -> "ResourceKey":
        if isinstance(__o, ResourceKey):
            self.key = self.key + SEPERATOR + __o.key
        elif isinstance(__o, str):
            self.key = self.key + SEPERATOR + __o
        return self

    def __radd__(self, __o: str | "ResourceKey") -> "ResourceKey":
        if isinstance(__o, ResourceKey):
            self.key = __o.key + SEPERATOR + self.key
        elif isinstance(__o, str):
            self.key = __o + SEPERATOR + self.key
        return self


class BaseField(Generic[T_Value]):
    key: ResourceKey
    nullable: bool
    description: Optional[str]

    _default: T_Value | None = None

    def __init__(
        self,
        key: ResourceKey | str,
        default: Optional[T_Value] = None,
        nullable=False,
        description: Optional[str] = None,
    ):
        if isinstance(key, ResourceKey):
            self.key = key
        elif isinstance(key, str):
            self.key = ResourceKey(key)
        else:
            raise TypeError(
                f"key must be a string or ResourceKey, not {type(key).__name__}"
            )
        self._default = default
        self.nullable = nullable
        self.description = description

    def init(self):
        raise NotImplementedError("Raw use of BaseField for annotation.")

    def setKey(self, key: str | ResourceKey) -> None:
        if isinstance(key, ResourceKey):
            self.key = key
        elif isinstance(key, str):
            self.key = ResourceKey(key)
        else:
            raise TypeError(
                f"key must be a string or ResourceKey, not {type(key).__name__}"
            )

    @property
    def value(self) -> Optional[T_Value]:
        return self.value

    @value.setter
    def value(self, value: Optional[T_Value]) -> None:
        warnings.warn(
            "Raw use of BaseField's value setter is not recommended.", UserWarning
        )
        self._value = value

    @value.deleter
    def value(self) -> None:
        warnings.warn(
            "Raw use of BaseField's value deleter is not recommended.", UserWarning
        )
        self._value = self._default

    def __repr__(self) -> str:
        return f"({str(self.__class__.__name__)}){self.key}"

    def __str__(self) -> str:
        return f"{self.__repr__()}[{self.description}]"

    def __enter__(self) -> Optional[T_Value]:
        return self.value

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        pass
