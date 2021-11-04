from nonebot.rule import ArgumentParser

from .handle import get_perm, edit_perm, list_perm, reset_perm, edit_plugin_perm

perm_parser = ArgumentParser("perm")

perm_subparsers = perm_parser.add_subparsers()

list_parser = perm_subparsers.add_parser("list")
list_parser.add_argument("-p", "--plugin", action="store_true", help="查看插件权限列表")
list_parser.add_argument("-g", "--group", action="store_true", help="查看群组权限列表")
list_parser.set_defaults(handle=list_perm)

get_parser = perm_subparsers.add_parser("get")
get_parser.add_argument("-u", "--user", action="store", nargs="+", default=[], type=int)
get_parser.add_argument("-g", "--group", action="store", nargs="+", default=[], type=int)
get_parser.set_defaults(handle=get_perm)

set_parser = perm_subparsers.add_parser("set")
set_parser.add_argument("perm", nargs=1)
set_parser.add_argument("-u", "--user", action="store", nargs="+", default=[], type=int)
set_parser.add_argument("-g", "--group", action="store", nargs="+", default=[], type=int)
set_parser.set_defaults(handle=edit_perm)

edit_parser = perm_subparsers.add_parser("edit")
edit_parser.add_argument("perm", nargs=1)
edit_parser.add_argument(
    "-p", "--plugins", action="store", nargs="+", default=[], type=str
)
edit_parser.set_defaults(handle=edit_plugin_perm)

reset_parser = perm_subparsers.add_parser("reset")
reset_parser.add_argument(
    "-u", "--user", action="store", nargs="+", default=[], type=int
)
reset_parser.add_argument(
    "-g", "--group", action="store", nargs="+", default=[], type=int
)
reset_parser.add_argument(
    "-p", "--plugin", action="store", nargs="+", default=[], type=str
)
reset_parser.set_defaults(handle=reset_perm)
