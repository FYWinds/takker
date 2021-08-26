import os
import re
import json
import random
import jieba
import jieba.analyse
from configs.path_config import VOICE_PATH, TEXT_PATH

v_dict: list[dict[str, str]] = []

voices = os.listdir(f"{VOICE_PATH}atri")
for v in voices:
    voice = re.findall("(.*).mp3", v)[0]
    voice_full_seg = " ".join(list(jieba.cut(voice)))
    voice_key_seg = " ".join(list(jieba.analyse.extract_tags(voice)))
    v_dict.append({"o": v, "s": voice, "s_f": voice_full_seg, "s_k": voice_key_seg})


json_file = open(f"{TEXT_PATH}atri.json", mode="w", encoding="utf-8")

json.dump(v_dict, json_file, indent=4, ensure_ascii=False)
