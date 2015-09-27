from flask import Flask
from flask_restful import Resource, Api
# from game import Game

app = Flask(__name__)
api = Api(app)


class CreateGame(Resource):
    def get(self):
        return {'gameid': 1}


class JoinGame(Resource):
    def get(self):
        return {'gameid': 1}


class Turn(Resource):
    def get(self):
        return {'turn': 1}

    def post(self):
        return {'turn': 1}


class GameInfo(Resource):
    def get(self):
        return {'gameid': 1,
                'players': ['none']}


api.add_resource(CreateGame, '/create')
api.add_resource(JoinGame, '/join')
api.add_resource(Turn, '/game/turn')
api.add_resource(GameInfo, '/game')

if __name__ == '__main__':
    app.run(debug=True)
