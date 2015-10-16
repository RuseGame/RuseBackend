import game


class MockEmitter:
    def update(self, cookie, player_dict):
        print("To", str(cookie)+":")
        print(player_dict)


def run_tests():
    emitter = MockEmitter()
    players = ["Rick", "Morty", "Troy", "Abed", "Yolo", "Solo"]
    test_cases = [("5 Players", players[:5])]

    for descrip, case in test_cases:
        print(descrip)
        ruse = game.Game(1, emitter)
        for cookie, name in enumerate(case):
            ruse.add_player(cookie, name)
        for cookie, player in ruse.players.items():
            move_list = [{"move_type": "send",
                          "to": player.target,
                          "from": player.alias,
                          "message": "Hi " + str(cookie)}]
            if cookie % 2 == 1:
                move_list.append({"move_type": "spoof",
                                  "to": player.alias,
                                  "from": player.target,
                                  "spoofer": player.alias,
                                  "message": "spoofed by " + player.alias})
            else:
                move_list.append({"move_type": "wiretap",
                                  "tapper": player.alias,
                                  "target": player.target,
                                  "direction": "outgoing"})
            ruse.process_moves(cookie, move_list)

        for cookie, player in ruse.players.items():
            move_list = []
            if cookie % 2 == 1:
                move_list.append({"move_type": "ambush",
                                  "attacker": player.alias,
                                  "target": "White"})
            else:
                move_list.append({"move_type": "spoof",
                                  "spoofer": player.alias,
                                  "to": player.alias,
                                  "from": player.target,
                                  "message": "spoofed by " + player.alias})
            ruse.process_moves(cookie, move_list)

        print("\n")


if __name__ == '__main__':
    run_tests()
