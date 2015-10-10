import game


class MockEmitter:
    def update(self, cookie, player_dict):
        print("To", str(cookie)+":")
        print(player_dict)


def run_tests():
    emitter = MockEmitter()
    players = ["Rick", "Morty", "Troy", "Abed", "Yolo", "Solo"]
    test_cases = [("5 Players", players[:5]),
                  ("Too Few (4) Players", players[:4]),
                  ("Too Many (6) Players", players)]

    for descrip, case in test_cases:
        print(descrip)
        ruse = game.Game(1, emitter)
        for cookie, name in enumerate(case):
            ruse.add_player(cookie, name)
        print("\n")


if __name__ == '__main__':
    run_tests()
