class Move:
    """
    Move Interface

    is_valid -- checks if the move is a valid move, returns True or False
    cost     -- the amount of points it costs to make the move
    """
    cost = None

    def is_valid(self):
        raise NotImplementedError

    def _alias_validate(self, *aliases):
        alias_list = ["Pink", "Green", "Blue", "White", "Orange"]
        for alias in aliases:
            if alias not in alias_list:
                return False
            alias_list.remove(alias)
        return True


class Message:
    def create_msg(self, player_from, player_to, text):
        self.message = {"from": player_from,
                        "to": player_to,
                        "text": text}

    def is_valid(self):
        player_from = self.message.get("from")
        player_to = self.message.get("to")
        return self._alias_validate(player_from, player_to)


class Send(Move, Message):
    """
    A Send command.

    Keyword arguments:
    mover     -- player object of the person making the move
    player_to -- player object of the recipient
    text      -- the message to send

    The sender cannot be the same as the recipient.
    """
    cost = 1

    def __init__(self, mover, player_to, text):
        super(Move).__init__()
        self.mover = mover
        super().__init__(mover, player_to, text)

    def is_valid(self):
        player_to = self.message.get("to")
        return self._alias_validate(self.mover, player_to)


class Spoof(Move):
    """
    A Spoof command.

    Keyword arguments:
    mover       -- player object of the person sending the spoofed message
    player_from -- player object of the spoofed sender
    player_to   -- player object of the spoof recipient
    text        -- the spoofed message to send

    Only requires that the spoofed message be valid.
    """
    cost = 2

    def __init__(self, mover, player_from, player_to, text):
        self.mover = mover
        self.message = Message(player_from, player_to, text)

    def is_valid(self):
        player_from = self.message.get("from")
        player_to = self.message.get("to")
        return self._alias_validate(player_from, player_to)


class Wiretap(Move):
    """
    A Wiretap command.

    Keyword arguments:
    mover     -- player object of the person placing the wiretap
    target    -- player object of the person being wiretapped
    direction -- direction of the wiretap

    The direction must be either 'incoming' or 'outgoing'.
    """
    cost = 3

    def __init__(self, mover, target, direction):
        self.mover = mover
        self.target = target
        self.direction = direction

    def is_valid(self):
        is_direction_valid = self.direction in ("incoming", "outgoing")
        return self._alias_validate(self.target) and is_direction_valid


class Ambush(Move):
    """
    An Ambush command.

    Keyword arguments:
    mover  -- player object of the person making the ambush
    target -- player object of the person being ambushed

    A player cannot ambush themself.
    """
    cost = 4

    def __init__(self, mover, target):
        self.mover = mover
        self.target = target

    def is_valid(self):
        return self._alias_validate(self.mover, self.target)


def move_factory(data):
    move_map = {"send": Send,
                "spoof": Spoof,
                "wiretap": Wiretap,
                "ambush": Ambush}
    move_spawner = move_map.get(data.get("move_type"))
    move = data.get("move")
    try:
        return move_spawner(**move)
    finally:
        return None
