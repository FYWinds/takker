from nonebot.rule import ArgumentParser

from .handle import handle_bind, handle_item, handle_stat, handle_uptime

wynn_parser = ArgumentParser("wynn")

wynn_subparsers = wynn_parser.add_subparsers()

bind_parser = wynn_subparsers.add_parser("bind")
bind_parser.add_argument("name", nargs="?")
bind_parser.set_defaults(handle=handle_bind)

stat_parser = wynn_subparsers.add_parser("stat")
stat_parser.add_argument("name", nargs="?")
stat_parser.add_argument("-v", "--verbose", action="store_true")
stat_parser.set_defaults(handle=handle_stat)

item_parser = wynn_subparsers.add_parser("item")
item_parser.add_argument("item", nargs="+")
item_parser.add_argument("-v", "--verbose", action="store_true")
item_parser.set_defaults(handle=handle_item)

uptime_parser = wynn_subparsers.add_parser("uptime")
uptime_parser.add_argument("server", nargs="*")
uptime_parser.add_argument("-sp", "--soulpoint", action="store_true")
uptime_parser.add_argument("-n", "--normal", action="store_true")
# uptime_parser.add_argument("-v", "--verbose", action="store_true")
uptime_parser.add_argument("-r", "--reverse", action="store_true")
uptime_parser.set_defaults(handle=handle_uptime)
