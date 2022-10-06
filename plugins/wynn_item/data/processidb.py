import json

with open("itemdb.json", "r", encoding="utf-8") as f:
    idb = json.load(f)

new_idb = []
for i in idb["items"]:
    new_idb.append(i["name"])

with open("processed_idb.json", "w", encoding="utf-8") as f:
    json.dump(new_idb, f, ensure_ascii=False, indent=4)
