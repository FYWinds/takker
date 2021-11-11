import json

from nonebot.log import logger

from configs.path_config import TEXT_PATH

fortune: list[dict]
msg_of_day: list[dict]
atri_text: list[dict]
book_of_answers: list[str]


with open(f"{TEXT_PATH}fortune.json", "r", encoding="utf-8") as file:
    fortune = json.load(file)["data"]

with open(f"{TEXT_PATH}msg_of_day.json", "r", encoding="utf-8") as file:
    msg_of_day = json.load(file)["data"]

with open(f"{TEXT_PATH}atri.json", "r", encoding="utf-8") as file:
    atri_text = json.load(file)

with open(f"{TEXT_PATH}book_of_answers.json", "r", encoding="utf-8") as file:
    book_of_answers = json.load(file)


class ProcessTime:
    def __init__(self, plugin_name: str, time: int):
        self.name = plugin_name
        self.time = time
        self.count = 1

    def add_time(self, time: int):
        self.time = (self.time * self.count + time) / (self.count + 1)
        self.count += 1

    def get_time(self):
        return self.time


process_time: dict[str, ProcessTime] = {}
