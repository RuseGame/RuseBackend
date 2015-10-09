NUM_PLAYERS = 5


class Game:
    def __init__(self, game_id, emitter):
        self.game_id = game_id
        self.emitter = emitter
        self.players = []
        self.turns = []

    def add_player(self, player_cookie):
        pass

    def start_game(self):
        pass

    def process_moves(self):
        pass

    def resolve_turn(self):
        pass


class Player:
    def __init__(self, cookie, name):
        self.cookie = cookie
        self.name = name
        self.inbox = []
        self.outbox = []


class Turn:
    def __init__(self, turn_number):
        self.turn_number = turn_number
        self.submitted = [False] * NUM_PLAYERS
        self.messages = []
        self.wiretaps = []
        self.attacks = []


class Move:
    def __init__(self, data):
        self.data = data
