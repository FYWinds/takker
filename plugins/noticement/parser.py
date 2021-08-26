from nonebot.rule import ArgumentParser

from .handle import handle_ls, handle_send

n_parser = ArgumentParser("notice")

n_subparsers = n_parser.add_subparsers()

list_parser = n_subparsers.add_parser("list")
list_group = list_parser.add_mutually_exclusive_group()
list_parser.set_defaults(handle=handle_ls)

send_parser = n_subparsers.add_parser("send")
send_parser.add_argument("groups", nargs="*")
send_parser.add_argument(
    "-n", "--notice", action="store", nargs="+", default=[], type=str
)
send_parser.set_defaults(handle=handle_send)
