import sys, os
sys.path.insert(1, "/".join(os.path.realpath(__file__).split("/")[0:-2]))

from card import Card


def test_create():
    card = Card.create_from_path("shahaf", "creator", "test.jpeg", "riddle", "solution")
    image_before = card.image.image.tobytes()
    card.image.encrypt(card.solution)
    data = card.serialize()
    card2 = Card.deserialize(data)
    if card2.image.decrypt("solution"): 
        card2.solution = "solution"

    assert(repr(card) == repr(card2))
    assert image_before == card2.image.image.tobytes()