"""
Author: FYWindIsland
Date: 2021-08-16 22:22:53
LastEditTime: 2021-08-21 14:49:56
LastEditors: FYWindIsland
Description: 
I'm writing SHIT codes
"""
import os
import re
import random
from typing import List
from configs.path_config import VOICE_PATH

voices: List[str] = os.listdir(f"{VOICE_PATH}dinggong")
voice = random.choice(voices)
text = re.findall("_(.*)_", voice)

print(text)
