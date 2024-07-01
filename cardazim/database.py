import pymongo

class DatabaseSaver:
    def __init__(self,url) -> None:
        myclient = pymongo.MongoClient(url)
        mydb = myclient["cardazim_database"]

        self.solved = mydb["solved_cards"]
        self.unsolved = mydb["unsolved_cards"]

    def save(self, data, path):
        if (path == "./static/solved_cards"):
            self.solved.insert_one(data)
        elif (path == "./static/unsolved_cards"):
            self.unsolved.insert_one(data)
        else:
            raise ValueError("Invalid path")
    def load_unsolved(self, path):
        cards_data_array = []
        for card in self.unsolved.find():
            image_path = card["image_path"]
            with open(image_path, "rb") as f:
                cards_data_array.append(f.read())
        return cards_data_array
    def load_metadata(self, path):
        metadata = []
        # print(path)
        if (path == "./static/solved_cards"):
            db = self.solved
        elif (path == "./static/unsolved_cards"):
            db = self.unsolved
        else:
            raise ValueError("Invalid path")
        for card in db.find():
            metadata.append(card)
        return metadata

def insert_one(mydb,mycol):
    mydict = { "name": "John", "address": "Highway 37" }
    x = mycol.insert_one(mydict)
    print(x.inserted_id)

def list_all(mydb,mycol):
    for x in mycol.find():
        print(x)
    
def list_database(mydb,mycol):
    for x in myclient.list_database_names():
        print(x)

def rm_all(mydb, mycol):
    mycol.delete_many({})

def rm_database(myclient):
    myclient.drop_database("cardazim_database")



if (__name__ == "__main__"):
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["cardazim_database"]

    solved = mydb["solved_cards"]
    unsolved = mydb["unsolved_cards"]

    print("listing all solved cards")
    list_all(mydb, solved)
    print("listing all unsolved cards")
    list_all(mydb, unsolved)

    # insert_one(mydb,mycol)
    # list_all(mydb, mycol)
    # rm_all()
    # list_all()
    # list_database() 
    # rm_database(myclient)