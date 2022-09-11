from nonebot.rule import ArgumentParser

from .handle import ls, add, remove, settings

bs_parser = ArgumentParser("bs")

bs_subparsers = bs_parser.add_subparsers()


list_parser = bs_subparsers.add_parser(
    "list", aliases=["主播列表", "列表", "主播", "up", "UP", "up主", "UP主"]
)
list_parser.add_argument("-u", "--user", action="store", nargs="+", default=[], type=int)
list_parser.add_argument(
    "-g", "--group", action="store", nargs="+", default=[], type=int
)
list_parser.add_argument("-a", "--all", action="store_true")
list_parser.set_defaults(handle=ls)


add_parser = bs_subparsers.add_parser("add", aliases=["添加主播", "关注", "添加"])
add_parser.add_argument("bid", nargs="*")
add_parser.add_argument("-u", "--user", action="store", nargs="+", default=[], type=int)
add_parser.add_argument("-g", "--group", action="store", nargs="+", default=[], type=int)
add_parser.set_defaults(handle=add)

remove_parser = bs_subparsers.add_parser("remove", aliases=["删除主播", "取关", "删除"])
remove_parser.add_argument("bid", nargs="*")
remove_parser.add_argument(
    "-u", "--user", action="store", nargs="+", default=[], type=int
)
remove_parser.add_argument(
    "-g", "--group", action="store", nargs="+", default=[], type=int
)
remove_parser.set_defaults(handle=remove)

# *主播设置相关指令 bs set <bid>
# !皆为直接切换状态
settings_parser = bs_subparsers.add_parser("set", aliases=["设置", "主播设置", "选项"])
settings_parser.add_argument("bid", nargs="*")
settings_parser.add_argument(
    "-u", "--user", action="store", nargs="+", default=[], type=int
)
settings_parser.add_argument(
    "-g", "--group", action="store", nargs="+", default=[], type=int
)
settings_parser.add_argument("-a", "--at", action="store_true")
settings_parser.add_argument("-l", "--live", action="store_true")
settings_parser.add_argument("-d", "--dynamic", action="store_true")
settings_parser.set_defaults(handle=settings)
