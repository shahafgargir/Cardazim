# Template-Repository

This is a template for the Cardazim Project!
Feel free to look around for interesting stuff!

Start the Card server:
python3 server.py 127.0.0.1 8080 ./static/unsolved_cards

example for client:
python3 client.py "Guess My Name" "Shelly Rimon" "What is my name?" "Shelly" ./test.jpeg

run solver:
python3 solver.py ./static/unsolved_cards ./static/solved_cards

run database docker:
docker run -d -p 27017:27017 --name cardb mongo

run python server:
python3 API.py


requirements:
pip install PyCryptodome
pip install pymongo
pip install flask
pip install pillow
pip install furl
pip install npyscreen