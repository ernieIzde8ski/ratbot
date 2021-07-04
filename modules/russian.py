import json
from pathlib import Path

path = Path("../data/russian.json")
print(path)

with open(path, "r", encoding="utf-8-sig") as file:
    data = json.load(file)
    verses = []
    for book in data:
        for chapter in book["chapters"]:
            for verse in chapter:
                verses.append(verse)
        # prevent the bible from getting *too* large
        if len(verses) > 10000:
            break

with open(path, "w+", encoding="utf-8") as file:
    json.dump(verses, file)
    print("Converted Russian bible to proper format")
