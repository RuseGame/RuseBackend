from random import shuffled, shuffle, choice

NUM_PLAYERS = 5
ALIASES = ["Pink", "Green", "Blue", "White", "Orange"]


class Game:
    """
    An object to contain an entire game of Ruse.
    """

    def __init__(self, game_id, emitter):
        self.game_id = game_id
        self.emitter = emitter
        self.players = {}
        self.turns = []

    def add_player(self, player_cookie, nickname):
        """
        Adds the player to the game.
        Fails if:
            5 players already joined or
            player already joined
        """

        if len(self.players.keys()) > 4:
            return False
        if player_cookie in self.players:
            return False
        player = Player(player_cookie, nickname)
        self.players[player_cookie] = player

        if len(self.players.keys()) == 5:
            self.start_game()
        return True

    def start_game(self):
        """
        Give everyone an alias and target, then start the turn
        """

        aliases = shuffled(ALIASES[:])
        for player in self.players:
            player.alias = aliases.pop()

        shuffle(self.players)
        for i in range(len(self.players)-1):
            self.players[i].target = self.players[i+1].alias
        self.players[-1].target = self.players[0].alias

        # TODO: send initial messages

    def start_turn(self):
        # TODO: send turn start message
        pass

    def process_moves(self, player_cookie, move_list):
        pass

    def resolve_turn(self):
        pass


class Player:
    def __init__(self, cookie, nickname):
        self.cookie = cookie
        self.name = nickname
        self.honorific = choice(["Mr.", "Ms."])
        self.inbox = []
        self.outbox = []
        self.alias = None
        self.target = None

    def __str__(self):
        return self.honorific + " " + self.alias


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
