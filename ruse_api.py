from flask import Flask, jsonify
from game import Game
app = Flask(__name__)

games = {}
game_id_counter = 0


@app.route('/')
def hello_world():
    return jsonify({"hello": "world"})


@app.route('/games')
def get_games():
    global games
    return jsonify({"current games": str(games.keys())})


@app.route('/games/create')
def make_game():
    global game_id_counter
    game_id_counter += 1
    games[str(game_id_counter)] = Game(game_id_counter)
    return jsonify({"game_id": str(game_id_counter)})

if __name__ == '__main__':
    app.run()
