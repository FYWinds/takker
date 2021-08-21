"""
Author: FYWindIsland
Date: 2021-08-16 22:22:53
LastEditTime: 2021-08-21 17:18:53
LastEditors: FYWindIsland
Description: 
I'm writing SHIT codes
"""
import os
import re
import random
from configs.path_config import VOICE_PATH

voices: dict[str, int] = {"test": 0, "test1": 5, "test3": 1}

print(dict(sorted(voices.items(), key=lambda item: item[1])))
