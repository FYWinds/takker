from nonebot.rule import ArgumentParser

from .handle import handle_get, handle_set

pic_parser = ArgumentParser("pix")

pic_parser.add_argument("keywords", nargs="*")
pic_parser.add_argument("-l", "--level", action="store", nargs=1, default=[], type=int)
pic_parser.set_defaults(handle=handle_get)

set_parser = ArgumentParser("pixset")
set_parser.add_argument("state", nargs=1, default=[], type=int)
set_parser.add_argument("-s", "--settings", action="store", nargs="+", type=str)
set_parser.set_defaults(handle=handle_set)
