import mock
from nonebot.plugin.manager import (
    Optional,
    ModuleType,
    PluginMetadata,
    _managers,
    _new_plugin,
    _revert_plugin,
    _current_plugin_chain,
)

from . import escape


# Patched exec_module
def exec_module(self, module: ModuleType) -> None:
    if self.loaded:
        return

    # create plugin before executing
    plugin = _new_plugin(self.name, module, self.manager)
    setattr(module, "__plugin__", plugin)

    # detect parent plugin before entering current plugin context
    parent_plugins = _current_plugin_chain.get()
    for pre_plugin in reversed(parent_plugins):
        if _managers.index(pre_plugin.manager) < _managers.index(self.manager):
            plugin.parent_plugin = pre_plugin
            pre_plugin.sub_plugins.add(plugin)
            break

    # enter plugin context
    _plugin_token = _current_plugin_chain.set(parent_plugins + (plugin,))

    try:
        super().exec_module(module)  # type: ignore
    except Exception:
        _revert_plugin(plugin)
        raise
    finally:
        # leave plugin context
        _current_plugin_chain.reset(_plugin_token)

    # get plugin metadata
    metadata: Optional[PluginMetadata] = escape(getattr(module, "__plugin_meta__", None))
    plugin.metadata = metadata

    return


mock.patch("nonebot.plugin.manager.PluginLoader.exec_module", exec_module)
