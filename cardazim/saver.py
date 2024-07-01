import json
import os
from card import Card
from furl import furl
from database import DatabaseSaver
'''
 f = furl('http://user:pass@www.google.com:99/')
f.scheme, f.username, f.password, f.host, f.port
('http', 'user', 'pass', 'www.google.com', 99)
'''
class FileSystemSaver:
    def save(self, data, path):
        path = path + "/" + data["name"]
        with open(path + "/metadata.json", 'w') as f:
            json_data = json.dumps(data)
            f.write(json_data)
    def load_unsolved(self, unsolved_path):
        cards_data_array = []
        for card in os.listdir(unsolved_path):
            if (card[0] == "."):
                continue
            with open(unsolved_path + "/" + card + "/metadata.json", "r") as f:
                j = json.load(f)
            with open(j["image_path"], "rb") as f:
                cards_data_array.append(f.read())
        return cards_data_array
    def load_metadata(self, path):
        metadata = []
        for card in os.listdir(path):
            if (card[0] == "."):
                continue
            with open(path + "/" + card + "/metadata.json", "r") as f:
                metadata.append(json.load(f))
        return metadata


def get_driver(driver_url):
    f = furl(driver_url)
    if f.scheme == "fs":
        return FileSystemSaver()
    if f.scheme == "mongodb":
        return DatabaseSaver(driver_url)
    else:
        raise ValueError("Invalid drive type")

class Saver:
    # def __init__(self, driver_url = "fs://") -> None:
    def __init__(self, driver_url = "mongodb://localhost:27017/") -> None:
        self.driver = get_driver(driver_url)

    def save(self, card : Card, dir_path="."):
        # print(card)
        path = dir_path + "/" + card.name
        os.mkdir(path)
        
        image_path = path + "/image.jpg"
        key_hash = card.image.key_hash
        if (key_hash != None):
            key_hash = key_hash.decode("latin-1")
            with open (path + "/image.jpg", "wb") as f:
                f.write(card.serialize())
        else:
            card.image.image.save(path + "/image.jpg")
        
            
        data = {
                    "name": card.name,
                    "creator": card.creator, 
                    "riddle": card.riddle, 
                    "solution": card.solution,
                    "image_path": image_path
                }
        self.driver.save(data, dir_path)
    def load_unsolved_cards(self, path):
        card_dict = []
        cards_data_array = self.driver.load_unsolved(path)
        for card_data in cards_data_array:
            # card = Card.create_from_path(card_data["name"], card_data["creator"], card_data["image_path"], card_data["riddle"], card_data["solution"], card_data["key_hash"].encode("latin-1"))
            card = Card.deserialize(card_data)
            card_dict.append(card)
        return card_dict
    def load_metadata(self, path):
        return self.driver.load_metadata(path)


    # @classmethod
    # def save_unsolved(cls, card : Card, dir_path="."):
    #     data = card.serialize()

    #     dirs = [int(num) for num in os.listdir(dir_path) if num.isdigit()]
    #     if len(dirs) == 0:
    #         file_name = "0"
    #     else:
    #         file_name = str(max(dirs) + 1)

    #     path = dir_path + "/" + file_name

    #     with open(path, 'wb') as f:
    #         data = card.serialize()
    #         f.write(data)