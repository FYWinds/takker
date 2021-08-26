from nonebot.rule import ArgumentParser

from .handle import handle_ls, handle_ban, handle_unban

pm_parser = ArgumentParser("pm")

pm_subparsers = pm_parser.add_subparsers()

list_parser = pm_subparsers.add_parser("list")
list_group = list_parser.add_mutually_exclusive_group()
list_group.add_argument(
    "-u", "--user", action="append", nargs="?", default=[], type=int
)
list_group.add_argument(
    "-g", "--group", action="append", nargs="?", default=[], type=int
)
list_parser.add_argument("-a", "--all", action="store_true")
list_parser.set_defaults(handle=handle_ls)

ban_parser = pm_subparsers.add_parser("ban")
ban_parser.add_argument("plugin", nargs="*")
ban_parser.add_argument("-a", "--all", action="store_true")
ban_parser.add_argument("-r", "--reverse", action="store_true")
ban_parser.add_argument("-u", "--user", action="store", nargs="+", default=[], type=int)
ban_parser.add_argument(
    "-g", "--group", action="store", nargs="+", default=[], type=int
)
ban_parser.set_defaults(handle=handle_ban)

unban_parser = pm_subparsers.add_parser("unban")
unban_parser.add_argument("plugin", nargs="*")
unban_parser.add_argument("-a", "--all", action="store_true")
unban_parser.add_argument("-r", "--reverse", action="store_true")
unban_parser.add_argument(
    "-u", "--user", action="store", nargs="+", default=[], type=int
)
unban_parser.add_argument(
    "-g", "--group", action="store", nargs="+", default=[], type=int
)
unban_parser.set_defaults(handle=handle_unban)
