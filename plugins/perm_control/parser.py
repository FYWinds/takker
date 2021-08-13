"""
Author: FYWindIsland
Date: 2021-08-11 16:16:38
LastEditTime: 2021-08-13 09:43:57
LastEditors: FYWindIsland
Description: 
I'm writing SHIT codes
"""
from nonebot.rule import ArgumentParser

from .handle import list_perm, get_perm, edit_perm

perm_parser = ArgumentParser("perm")

perm_subparsers = perm_parser.add_subparsers()

list_parser = perm_subparsers.add_parser("list")
list_group = list_parser.add_mutually_exclusive_group()
list_parser.set_defaults(handle=list_perm)

get_parser = perm_subparsers.add_parser("get")
get_parser.add_argument("-u", "--user", action="store", nargs="+", default=[], type=int)
get_parser.add_argument(
    "-g", "--group", action="store", nargs="+", default=[], type=int
)
get_parser.set_defaults(handle=get_perm)

set_parser = perm_subparsers.add_parser("set")
set_parser.add_argument("perm", nargs=1)
set_parser.add_argument("-u", "--user", action="store", nargs="+", default=[], type=int)
set_parser.add_argument(
    "-g", "--group", action="store", nargs="+", default=[], type=int
)
set_parser.set_defaults(handle=edit_perm)
