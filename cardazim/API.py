from flask import Flask, jsonify, send_file

from saver import Saver

database_url = ''
saver = None
app = Flask(__name__)

def card_info(card):
    info = "name" + card["name"]
    info +="creator" + card["creator"]
    info += "riddle" + card["riddle"]
    
    info += "solution" + card["solution"]
    info += "image_path" + card["image_path"]
    return info

@app.route('/creators') 
def list_of_creator():
    global saver 
    creators = [card["creator"] for card in saver.load_metadata("./solved_cards")]
    creators += [card["creator"] for card in saver.load_metadata("./unsolved_cards")]
    creators = list(dict.fromkeys(creators))
    return jsonify(creators)

# @app.route('/cats/<string:cat_name>') 


@app.route('/creators/<string:creator>/cards')
def solved_cards_from_creator(creator):
    creators = saver.load_metadata("./solved_cards")
    cards = [card for card in creators if card["creator"] == creator]
    return jsonify([card["name"] for card in cards])
    return jsonify(cats[cat_name])
@app.route('/creators/<string:creator>/cards/<string:card_name>')
def get_card_info(creator, card_name):
    creators = saver.load_metadata("./solved_cards")
    cards = [card for card in creators if card["creator"] == creator]
    cards = [card for card in cards if card["name"] == card_name]
    for card in cards:
        del card["_id"]
    return jsonify(cards)

@app.route('/creators/<string:creator>/cards/<string:card_name>/image.jpg')
def get_image(creator, card_name):
    creators = saver.load_metadata("./solved_cards")
    cards = [card for card in creators if card["creator"] == creator]
    cards = [card for card in cards if card["name"] == card_name]
    if (len(cards) == 0):
        return "Card not found", 404
    return send_file(cards[0]["image_path"], mimetype='image/gif')

def run_api_server(host, port, database_url = 'mongodb://127.0.0.1:27017'):
    global saver
    saver = Saver(database_url)
    app.run(host=host, port=port)
    

if __name__ == '__main__':
    run_api_server('127.0.0.1', 5000)