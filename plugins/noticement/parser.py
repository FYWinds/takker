"""
Author: FYWindIsland
Date: 2021-08-13 09:24:01
LastEditTime: 2021-08-13 10:12:44
LastEditors: FYWindIsland
Description: 
I'm writing SHIT codes
"""
from nonebot.rule import ArgumentParser

from .handle import handle_ls, handle_send

n_parser = ArgumentParser("notice")

n_subparsers = n_parser.add_subparsers()

list_parser = n_subparsers.add_parser("list")
list_group = list_parser.add_mutually_exclusive_group()
list_parser.set_defaults(handle=handle_ls)

ban_parser = n_subparsers.add_parser("send")
ban_parser.add_argument("groups", nargs="*")
ban_parser.add_argument(
    "-n", "--notice", action="store", nargs="+", default=[], type=str
)
ban_parser.set_defaults(handle=handle_send)
