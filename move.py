def alias_validate(self, *aliases):
    """
    Takes n arguments,
    Returns True if all given args are valid, unique aliases
    Else returns False
    """
    alias_list = ["Pink", "Green", "Blue", "White", "Orange"]
    for alias in aliases:
        if alias not in alias_list:
            return False
        alias_list.remove(alias)
    return True


class Message:
    """
    Interface implementation for "messaging" moves (i.e. Send & Spoof)
    """
    def __init__(self, player_from, player_to, text):
        self.message = {"from": player_from,
                        "to": player_to,
                        "text": text}

    def is_valid(self):
        player_from = self.message.get("from")
        player_to = self.message.get("to")
        return alias_validate(player_from, player_to)


class Send(Message):
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
        self.mover = mover
        super().__init__(mover, player_to, text)


class Spoof(Message):
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
        super().__init__(player_from, player_to, text)


class Wiretap:
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
        return alias_validate(self.target) and is_direction_valid


class Ambush:
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
        return alias_validate(self.mover, self.target)


def move_factory(data):
    move_type = data.get("move_type")
    move = data.get("move")
    move_map = {"send": Send,
                "spoof": Spoof,
                "wiretap": Wiretap,
                "ambush": Ambush}
    move_spawner = move_map.get(move_type)
    try:
        return move_spawner(**move)
    except:
        return None
