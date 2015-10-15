from random import shuffle

NUM_PLAYERS = 5
ALIASES = ("Pink", "Green", "Blue", "White", "Orange")
MOVE_TYPES = ("send", "spoof", "wiretap", "ambush")


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

        aliases = list(ALIASES)
        shuffle(aliases)
        player_list = list(self.players.values())
        shuffle(player_list)

        for player in player_list:
            player.alias = aliases.pop()
        for i in range(len(player_list)-1):
            player_list[i].target = player_list[i+1].alias
        player_list[-1].target = player_list[0].alias

        for player in player_list:
            player.inbox[0].append("Hello " + str(player) + ",\n" +
                                   "Your target is Mr. " + player.target + ".")
            self.emitter.update(player.cookie, player._to_dict())
        self.start_turn()

    def start_turn(self):
        self.turns.append(Turn(len(self.turns)+1))
        for player in self.players.values():
            player.inbox.append([])

    def _validate_moves(self, mover_alias, move_list):
        action_points = 4
        other_players = [a for a in ALIASES if a != mover_alias]
        for move in move_list:
            move_type = move.get("move_type")
            if move_type in MOVE_TYPES:
                if move_type == "send":
                    send_from = move.get("from")
                    send_to = move.get("to")
                    if send_from != mover_alias or send_to not in other_players:
                        return False
                    action_points -= 1
                elif move_type == "spoof":
                    spoofed_from = move.get("from")
                    spoofed_to = move.get("to")
                    spoofer = move.get("spoofer")
                    if spoofer != mover_alias or spoofed_to == spoofed_from:
                        return False
                    if spoofed_to not in ALIASES or spoofed_from not in ALIASES:
                        return False
                    action_points -= 2
                elif move_type == "wiretap":
                    target = move.get("target")
                    tapper = move.get("tapper")
                    direction = move.get("direction")
                    if tapper != mover_alias or target not in ALIASES:
                        return False
                    if direction != "incoming" and direction != "outgoing":
                        return False
                    action_points -= 3
                elif move_type == "ambush":
                    target = move.get("target")
                    attacker = move.get("attacker")
                    if attacker != mover_alias or target not in other_players:
                        return False
                    action_points -= 4
            else:
                return False
        if action_points < 0:
            return False
        return True

    def process_moves(self, player_cookie, move_list):
        if self.turns == []:
            return False
        current_turn = self.turns[-1]
        submitting_player = self.players[player_cookie]
        if self._validate_moves(submitting_player.alias, move_list):
            if current_turn.submit(submitting_player.alias, move_list):
                if current_turn.missing_players() == set():
                    self.resolve_turn()
                return True
        return False

    def resolve_turn(self):
        ending_turn = self.turns[-1]
        alias_map = {player.alias: player
                     for player
                     in self.players.values()}
        for message in ending_turn.messages:
            report = "\"" + str(message.get("message")) + "\"\n- Mr. " + str(message.get("from"))
            alias_map[message.get("to")].inbox[-1].append(report)
        for wiretap in ending_turn.wiretaps:
            report = "From your wiretap:\n"
            in_out = "to" if wiretap.get("direction") == "incoming" else "from"
            for message in ending_turn.messages:
                if message.get(in_out) == wiretap.get("target"):
                    report += "Mr. " + str(message.get("to")) + ":\n" + str(message.get("message")) + "\n- Mr. " + str(message.get("from"))
            alias_map[wiretap.get("tapper")].inbox[-1].append(report)
        hits = {alias: []
                for alias
                in alias_map.keys()}
        for attack in ending_turn.attacks:
            hits[attack.get("target")].append(attack.get("attacker"))
        for target, attackers in hits.items():
            if len(attackers) > 1:
                alias_map[target].inbox[-1].append("You have been killed.")
                self.end_game()
                return
            elif len(attackers) > 0:
                alias_map[target].inbox[-1].append("You were unsucessfully attacked by Mr. " + attackers[0])
        for cookie, player in self.players.items():
            self.emitter.update(cookie, player._to_dict())
        self.start_turn()

    def end_game(self):
        for cookie, player in self.players.items():
            player.inbox.append(["Game Over."])
            self.emitter.update(cookie, player._to_dict())

class Player:
    def __init__(self, cookie, nickname):
        self.cookie = cookie
        self.name = nickname
        self.inbox = [[]]
        self.alias = None
        self.target = None

    def __str__(self):
        return "Mr. " + self.alias

    def _to_dict(self):
        return {
            "name": self.name,
            "inbox": self.inbox,
            "alias": self.alias,
            "target": self.target
        }


class Turn:
    def __init__(self, turn_number):
        self.turn_number = turn_number
        self.players = set(ALIASES)
        self.submitted = set()
        self.messages = []
        self.wiretaps = []
        self.attacks = []

    def submit(self, alias, moves):
        if alias not in self.submitted:
            for move in moves:
                move_type = move.get("move_type")
                if move_type == "send" or move_type == "spoof":
                    self.messages.append(move)
                elif move_type == "wiretap":
                    self.wiretaps.append(move)
                elif move_type == "ambush":
                    self.attacks.append(move)
            self.submitted.add(alias)
            return True
        return False

    def missing_players(self):
        return self.players - self.submitted
