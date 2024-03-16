from PIL import Image
from Crypto.Cipher import AES
import hashlib

class CryptImage:
    @classmethod
    def create_from_path(cls, path):
        with Image.open(path) as img:
            img.load()
        return cls(img,None)
    
    def __init__(self, image :Image, key_hash) -> None:
        self.image = image
        self.key_hash = key_hash
    
    def encrypt(self, key):
        AES_key = hashlib.sha256(key.encode()).digest()
        plainimage = self.image.tobytes()
        cipher = AES.new(AES_key, AES.MODE_EAX, nonce=b'arazim')
        self.image.frombytes(cipher.encrypt(plainimage))
        self.key_hash = hashlib.sha256(AES_key).digest()

    def decrypt(self,key):
        if (self.key_hash != hashlib.sha256(hashlib.sha256(key.encode()).digest()).digest()):
            return False
        
        AES_key = hashlib.sha256(key.encode()).digest()
        encrypt_image = self.image.tobytes()
        cipher = AES.new(AES_key, AES.MODE_EAX, nonce=b'arazim')
        self.image.frombytes(cipher.decrypt(encrypt_image))
        self.key_hash = None
        return True
        




# i = CryptImage.create_from_path("test.jpeg")
# i.encrypt("test")
# print(i.image.size)
# i.image.show()
# print(i.key_hash)
# print(i.decrypt("test"))
# i.image.show()
# print(i.key_hash)