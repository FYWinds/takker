import json
from typing import Any, Type, Optional
from dataclasses import field, dataclass

from pydantic import BaseModel
from nonebot.plugin import PluginMetadata as Nonebot_PluginMetadata


@dataclass(eq=False)
class UsageMetaData:
    """插件使用方法元信息"""

    usage: str
    """插件使用方法"""
    example: str
    """插件使用示例"""


@dataclass(eq=False)
class Usage:
    """插件使用方法"""

    user: Optional[UsageMetaData] = None
    """用户使用方法"""
    admin: Optional[UsageMetaData] = None
    """管理员使用方法"""
    superuser: Optional[UsageMetaData] = None
    """超级管理员使用方法"""

    extra: dict[str, UsageMetaData] = field(default_factory=dict)


@dataclass(eq=False)
class PluginMetadata:
    """插件元信息，由插件编写者提供"""

    name: str
    """插件可阅读名称"""
    description: str
    """插件功能介绍"""
    usage: Usage
    """插件使用方法"""
    config: Optional[Type[BaseModel]] = None
    """插件配置项"""
    version: Optional[str] = None
    """插件版本"""
    authors: Optional[list] = None
    """插件作者"""

    extra: dict[Any, Any] = field(default_factory=dict)


def escape(meta: Optional[PluginMetadata] = None) -> Optional[Nonebot_PluginMetadata]:
    """将 Takker 插件元信息转换为 NoneBot 插件元信息"""
    if not meta:
        return None
    meta.extra.update({"version": meta.version, "authors": meta.authors})
    return Nonebot_PluginMetadata(
        name=meta.name,
        description=meta.description,
        usage=json.dumps(meta.usage, ensure_ascii=False),
        config=meta.config,
        extra=meta.extra,
    )


def unescape(meta: Nonebot_PluginMetadata) -> PluginMetadata:
    """将 Takker 插件元信息转换为 Failsafe 插件元信息"""
    return PluginMetadata(
        name=meta.name,
        description=meta.description,
        usage=Usage(json.loads(meta.usage)),
        config=meta.config,
        version=meta.extra.get("version", None),
        authors=meta.extra.get("authors", None),
    )
