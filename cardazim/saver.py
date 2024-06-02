import json
import os
from card import Card

class Saver:
    @classmethod
    def save(cls, card : Card, dir_path="."):
        path = dir_path + "/" + card.name
        os.mkdir(path)
        card.image.image.save(path + "/image.jpg")

        with open(path + "/metadata.json", 'w') as f:

            image_path = path + "/image.jpg"

            data = {
                    "name": card.name,
                    "creator": card.creator, 
                    "riddle": card.riddle, 
                    "solution": card.solution, 
                    "image_path": image_path
                }

            json_data = json.dumps(data)
            f.write(json_data)


    @classmethod
    def save_unsolved(cls, card : Card, dir_path="."):
        dirs = [int(num) for num in os.listdir(dir_path) if num.isdigit()]
        if len(dirs) == 0:
            file_name = "0"
        else:
            file_name = str(max(dirs) + 1)

        path = dir_path + "/" + file_name

        with open(path, 'wb') as f:
            data = card.serialize()
            f.write(data)