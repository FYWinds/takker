import json

from nonebot.log import logger

FILE: str = "plugins/wynn/data.json"


def load_data() -> dict:
    with open(FILE, "rt", encoding="utf-8") as f:
        return json.loads(f.read())


data: dict = load_data()


def save_data(data: dict) -> None:
    # print(data)
    with open(FILE, "wt", encoding="utf-8") as f:
        f.write(json.dumps(data, indent=4, ensure_ascii=False))
    logger.debug("Wynncraft | Saved Data")


def get_data() -> dict:
    global data
    return data


def set_data(data_: dict) -> None:
    global data
    data = data_
    save_data(data)
