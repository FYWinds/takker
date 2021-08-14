"""
Author: FYWindIsland
Date: 2021-08-14 11:30:38
LastEditTime: 2021-08-14 12:01:56
LastEditors: FYWindIsland
Description: 
I'm writing SHIT codes
"""
from nonebot.rule import ArgumentParser

from .handle import handle_get

pic_parser = ArgumentParser("pix")

pic_parser.add_argument("keywords", nargs="*")
pic_parser.add_argument("-l", "--level", action="store", nargs=1, default=[], type=int)
pic_parser.set_defaults(handle=handle_get)
