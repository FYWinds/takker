"""
Author: FYWindIsland
Date: 2021-08-16 22:22:53
LastEditTime: 2021-08-20 17:42:21
LastEditors: FYWindIsland
Description: 
I'm writing SHIT codes
"""
from typing import *  # type: ignore

stats: Dict[int, Dict[str, int]] = {
    1: {"test": 1, "test1": 1},
    2: {"test": 0, "test1": 3},
}

ex: Dict[str, int] = {"test": 123, "test1": 4523}

time_today = 3


def test(time_today):
    if time_today in stats.keys():
        module_name = "test7"
        if module_name in stats[time_today].keys():
            stats[time_today].update({module_name: stats[time_today][module_name] + 1})
        else:
            stats[time_today].update({module_name: 1})
    else:
        module_name = "test5"
        stats.update({time_today: {module_name: 1}})


print(list(ex.values()))
print(stats)
