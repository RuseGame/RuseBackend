from flask import Flask, jsonify, Response, request, make_response
from game import Game
import time
app = Flask(__name__)

games = {}
game_eventers = {}
game_id_counter = 0
player_uid = 0


class ServerSideEventer:
    def __init__(self):
        self.maps = {}
        self.needs_update = {}

    def register(self, cookie):
        self.maps[cookie] = 0
        self.needs_update[cookie] = True

    def update(self, cookie, dictionary):
        pass

    def get_update(self, cookie):
        self.needs_update[cookie] = False
        return "success"


def event_stream(eventer, cookie):
    old = time.time()
    while True:
        new = time.time()
        if eventer.needs_update[cookie]:
            message = eventer.get_update(cookie)
            yield 'data: %s\n\n' % message
        if new - old > 5:
            old = new
            yield 'data: none\n\n'
        time.sleep(0.5)


@app.route('/')
def hello_world():
    global player_uid
    resp = make_response(jsonify({"hello": "world"}))
    if not request.cookies.get('player_id'):
        resp.set_cookie('player_id', str(player_uid))
        player_uid += 1
    return resp


@app.route('/games')
def get_games():
    global games
    return jsonify({"current games": str(games.keys())})


@app.route('/games/create')
def make_game():
    global game_id_counter, games, game_eventers
    game_id_counter += 1
    eventer = ServerSideEventer()
    eventer.register(request.cookies.get("player_id"))
    games[str(game_id_counter)] = Game(game_id_counter, eventer)
    game_eventers[str(game_id_counter)] = eventer
    return jsonify({"game_id": str(game_id_counter)})


@app.route('/<game_id>/stream')
def stream(game_id):
    global game_eventers
    player_cookie = request.cookies.get("player_id")
    return Response(event_stream(game_eventers[game_id], player_cookie),
                    mimetype="text/event-stream")

if __name__ == '__main__':
    app.debug = True
    app.run(threaded=True)
