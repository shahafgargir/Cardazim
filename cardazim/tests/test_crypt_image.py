import sys, os
sys.path.insert(1, "/".join(os.path.realpath(__file__).split("/")[0:-2]))

from crypt_image import CryptImage

def test_send_data():
    
    i = CryptImage.create_from_path("test.jpeg")
    i.encrypt("test")
    after_enc = i.image.size
    assert i.key_hash != None
    assert not i.decrypt("test2")
    assert i.decrypt("test")
    assert i.image.size == after_enc
    assert (i.key_hash == None)
