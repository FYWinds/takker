from nonebot.rule import ArgumentParser

from .handle import handle_get

pic_parser = ArgumentParser("pix")

pic_parser.add_argument("keywords", nargs="*")
pic_parser.add_argument("-l", "--level", action="store", nargs=1, default=[], type=int)
pic_parser.set_defaults(handle=handle_get)
