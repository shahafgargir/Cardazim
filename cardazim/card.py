from PIL import Image
from crypt_image import CryptImage
import struct

class Card:
    @classmethod
    def create_from_path(cls, name, creator, path, riddle, solution):
        image = CryptImage.create_from_path(path)
        return cls(name,creator,image,riddle,solution)
    

    def __init__(self,name,creator,image,riddle,solution) -> None:
        self.name = name
        self.creator = creator
        self.image = image
        self.riddle = riddle
        self.solution = solution

    def __repr__(self) -> str:
        return "<Card name={"+self.name+"}, creator={"+self.creator+"}>"
    
    def __str__(self) -> str:
        if (self.solution):
            return f"Card <{self.name}> by <{self.creator}>\nriddle: <{self.riddle}>\nsolution: <{self.solution}>"
        return f"Card <{self.name}> by <{self.creator}>\nriddle: <{self.riddle}>\nsolution: unsolved"

    def encript_card(self):    
        self.image.encrypt(self.solution)
    
    def serialize(self):
        data = b''
        data += struct.pack("<I",len(self.name.encode())) + self.name.encode()
        data += struct.pack("<I",len(self.creator.encode())) + self.creator.encode()
        data += struct.pack("<I", self.image.image.size[0])
        data += struct.pack("<I", self.image.image.size[1])
        data += self.image.image.tobytes()
        data += self.image.key_hash
        data += struct.pack("<I",len(self.riddle.encode())) + self.riddle.encode()
        return data
    
    @classmethod
    def get_str(cls,data):
        length = data[0:4]
        length = struct.unpack("<I",length)[0]
        string = data[4:4 + length].decode("utf8")
        return data[4 + length:], string

    @classmethod
    def deserialize(cls, data):
        data, name = cls.get_str(data)
        data, creator = cls.get_str(data)
        width, height = struct.unpack("<II",data[:8])
        image_data = data[8 : 3 * height * width + 8]
        data = data[3 * height * width + 8:]
        key_hash = data[:32]
        data, riddle = cls.get_str(data[32:])

        image = Image.frombytes("RGB",(width, height), image_data)
        CryptImage(image, key_hash)


        return cls(name, creator, CryptImage(image, key_hash), riddle, None)


# # print(Card())
# card = Card.create_from_path("shahaf", "creator", "test.jpeg", "riddle", "solution")
# card.image.encrypt(card.solution)
# data = card.serialize()
# card2 = Card.deserialize(data)

# if card2.image.decrypt("solution"): 
#     card2.solution = "solution"

# print(card)
# print(card2)
# assert(repr(card) == repr(card2))
# card2.image.image.show() # will show the same image as in path